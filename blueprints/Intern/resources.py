import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Intern
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#password Encription
from password_strength import PasswordPolicy
#Blueprint Collection
from blueprints.Company.model import Company
from blueprints.Certificate.model import Certificate
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task
from blueprints.OngoingPosition.model import OngoingPosition

# 'intern' penamaan (boleh diganti)
bp_intern = Blueprint('intern', __name__)
api = Api(bp_intern)

class InternResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        qry = Intern.query.get(args["id"])
        if qry is not None:
            return {"status":"success", "result":marshal(qry, Intern.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('image', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('pendidikan', location='json')
        parser.add_argument('deskripsi', location='json')

        parser.add_argument('kecamatan', location='json')
        parser.add_argument('kabupaten', location='json')
        parser.add_argument('desa_kelurahan', location='json')
        parser.add_argument('rt', location='json')
        parser.add_argument('rw', location='json')
        parser.add_argument('nik', location='json')
        parser.add_argument('jenis_kelamin', location='json')
        parser.add_argument('tempat_lahir', location='json')
        parser.add_argument('tanggal_lahir', location='json')
        parser.add_argument('jurusan', location='json')
        parser.add_argument('status_perkawinan', location='json')
        parser.add_argument('nama_ayah', location='json')
        parser.add_argument('nama_ibu', location='json')
        parser.add_argument('nama_perusahaan', location='json')
        parser.add_argument('jabatan', location='json')
        parser.add_argument('mulai_tahun', location='json')
        parser.add_argument('lama_kerja', location='json')
        parser.add_argument('provinsi', location='json')
        parser.add_argument('kota_kabupaten', location='json')
        parser.add_argument('kecamatan_penempatan', location='json')
        parser.add_argument('desa_kelurahan_penempatan', location='json')
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            intern = Intern(datetime.datetime.now(), args['name'], password_digest, args['image'], args['address'], True, 'intern', args['email'], args['pendidikan'], args['deskripsi'], args['kecamatan'], args['kabupaten'], args['desa_kelurahan'], args['rt'], args['rw'], args['nik'], args['jenis_kelamin'], args['tempat_lahir'], args['tanggal_lahir'], args['jurusan'], args['status_perkawinan'], args['nama_ayah'], args['nama_ibu'], args['nama_perusahaan'], args['jabatan'], args['mulai_tahun'], args['lama_kerja'], args['provinsi'], args['kota_kabupaten'], args['kecamatan_penempatan'], args['desa_kelurahan_penempatan'])
            
            try:
                db.session.add(intern)
                db.session.commit()
            except Exception as e:
                return {"status":"failed", "result": "intern already exist"}, 400, {'Content-Type':'application/json'}

            app.logger.debug('DEBUG : %s ', intern )

            return {"status":"success", "result":marshal(intern, Intern.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {"status":"failed", "result": "Wrong Password Length"}, 400, {'Content-Type':'application/json'}
    
    @jwt_required
    @intern_only
    def put(self):
        claims = get_jwt_claims()

        qry = Intern.query.get(claims["id"])

        if qry is None:
            return {'status':'failed',"result":"id not found"}, 404, {'Content-Type':'application/json'}

        defaultdata = marshal(qry, Intern.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', default=defaultdata["name"])
        parser.add_argument('image', location='json', default=defaultdata["image"])
        parser.add_argument('address', location='json', default=defaultdata["address"])
        parser.add_argument('pendidikan', location='json', default=defaultdata["pendidikan"])
        parser.add_argument('deskripsi', location='json', default=defaultdata["deskripsi"])
        args = parser.parse_args()

        qry.name = args["name"]
        qry.image = args["image"]
        qry.address = args["address"]
        qry.pendidikan = args["pendidikan"]
        qry.deskripsi = args["deskripsi"]

        db.session.commit()

        return {"status":"success", "result":marshal(qry, Intern.response_field)}, 200, {'Content-Type':'application/json'}

class InternList(Resource):

    def options(self):
        return {},200

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Intern.query

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Intern.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

class InternSpecialCase(Resource):

    def options(self):
        return {},200

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument("kecamatan", location = "args")
        parser.add_argument("kabupaten", location = "args")
        parser.add_argument("kota_kabupaten", location = "args")
        parser.add_argument("pendidikan", location = "args")
        parser.add_argument("jurusan", location = "args")
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Intern.query

        if args['kecamatan'] is not None:
            qry = qry.filter(Intern.kecamatan.like("%"+args["kecamatan"]+"%"))
        if args['kabupaten'] is not None:
            qry = qry.filter(Intern.kabupaten.like("%"+args["kabupaten"]+"%"))
        if args['kota_kabupaten'] is not None:
            qry = qry.filter(Intern.kota_kabupaten.like("%"+args["kota_kabupaten"]+"%"))
        if args['pendidikan'] is not None:
            qry = qry.filter(Intern.pendidikan.like("%"+args["pendidikan"]+"%"))
        if args['jurusan'] is not None:
            qry = qry.filter(Intern.jurusan.like("%"+args["jurusan"]+"%"))

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            internValue = marshal(row,Intern.response_field)

            OnPosQry = OngoingPosition.query.filter_by(intern_id=internValue["id"]).all()
            CertificateQry = Certificate.query.filter_by(intern_id=internValue["id"]).all()

            OnPosQryValue = marshal(OnPosQry, OngoingPosition.response_field)
            CertQryValue = marshal(CertificateQry,Certificate.response_field)

            internValue["position_history"] = OnPosQryValue
            internValue["certificate"] = CertQryValue

            result.append(internValue)
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}


api.add_resource(InternResource, '', '')
api.add_resource(InternList,'','/list')
api.add_resource(InternSpecialCase,'','/specialmetadata')