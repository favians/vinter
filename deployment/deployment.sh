cd $DEPLOYMENT_APP_PATH

git checkout master
git pull

sudo docker-compose down
sudo docker-compose up --build -d
