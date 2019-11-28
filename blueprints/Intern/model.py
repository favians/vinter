from blueprints import db
from flask_restful import fields


class Intern(db.Model):
    __tablename__ = "interns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    role = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(1024), nullable=True)
    pendidikan = db.Column(db.String(1024), nullable=True)
    deskripsi = db.Column(db.String(2048), nullable=True)

    kecamatan = db.Column(db.String(255), nullable=True)
    kabupaten = db.Column(db.String(255), nullable=True)
    desa_kelurahan = db.Column(db.String(255), nullable=True)
    rt = db.Column(db.Integer, nullable=True)
    rw = db.Column(db.Integer, nullable=True)
    nik = db.Column(db.Integer, nullable=True)
    jenis_kelamin = db.Column(db.String(255), nullable=True)
    tempat_lahir = db.Column(db.String(255), nullable=True)
    tanggal_lahir = db.Column(db.String(255), nullable=True)
    jurusan = db.Column(db.String(255), nullable=True)
    status_perkawinan = db.Column(db.String(255), nullable=True)
    nama_ayah = db.Column(db.String(255), nullable=True)
    nama_ibu = db.Column(db.String(255), nullable=True)
    nama_perusahaan = db.Column(db.String(255), nullable=True)
    jabatan = db.Column(db.String(255), nullable=True)
    mulai_tahun = db.Column(db.String(255), nullable=True)
    lama_kerja = db.Column(db.String(255), nullable=True)
    provinsi = db.Column(db.String(255), nullable=True)
    kota_kabupaten = db.Column(db.String(255), nullable=True)
    kecamatan_penempatan = db.Column(db.String(255), nullable=True)
    desa_kelurahan_penempatan = db.Column(db.String(255), nullable=True)



    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'name': fields.String,
        'image': fields.String,
        'address': fields.String,
        'active': fields.Boolean,
        'role': fields.String,
        'email': fields.String,
        'pendidikan': fields.String,
        'deskripsi': fields.String,

        'kecamatan' : fields.String,
        'kabupaten' : fields.String,
        'desa_kelurahan' : fields.String,
        'rt' : fields.Integer,
        'rw' : fields.Integer,
        'nik' : fields.Integer,
        'jenis_kelamin' : fields.String,
        'tempat_lahir' : fields.String,
        'tanggal_lahir' : fields.String,
        'jurusan' : fields.String,
        'status_perkawinan' : fields.String,
        'nama_ayah' : fields.String,
        'nama_ibu' : fields.String,
        'nama_perusahaan' : fields.String,
        'jabatan' : fields.String,
        'mulai_tahun' : fields.String,
        'lama_kerja' : fields.String,
        'provinsi' : fields.String,
        'kota_kabupaten' : fields.String,
        'kecamatan_penempatan' : fields.String,
        'desa_kelurahan_penempatan' : fields.String
    }

    def __init__(self, created_at, name, password, image, address, active, role, email, pendidikan, deskripsi, kecamatan, kabupaten, desa_kelurahan, rt, rw, nik, jenis_kelamin, tempat_lahir, tanggal_lahir, jurusan, status_perkawinan, nama_ayah, nama_ibu, nama_perusahaan, jabatan, mulai_tahun, lama_kerja, provinsi, kota_kabupaten, kecamatan_penempatan, desa_kelurahan_penempatan):
        self.created_at = created_at
        self.name = name
        self.password = password
        self.image = image
        self.address = address
        self.active = active
        self.role = role
        self.email = email
        self.pendidikan = pendidikan
        self.deskripsi = deskripsi

        self.kecamatan = kecamatan
        self.kabupaten = kabupaten
        self.desa_kelurahan = desa_kelurahan
        self.rt = rt
        self.rw = rw
        self.nik = nik
        self.jenis_kelamin = jenis_kelamin
        self.tempat_lahir = tempat_lahir
        self.tanggal_lahir = tanggal_lahir
        self.jurusan = jurusan
        self.status_perkawinan = status_perkawinan
        self.nama_ayah = nama_ayah
        self.nama_ibu = nama_ibu
        self.nama_perusahaan = nama_perusahaan
        self.jabatan = jabatan
        self.mulai_tahun = mulai_tahun
        self.lama_kerja = lama_kerja
        self.provinsi = provinsi
        self.kota_kabupaten = kota_kabupaten
        self.kecamatan_penempatan = kecamatan_penempatan
        self.desa_kelurahan_penempatan = desa_kelurahan_penempatan


    def __repr__(self):
        return '<Intern %r>' % self.id