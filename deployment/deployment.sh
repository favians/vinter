cd $DEPLOYMENT_APP_PATH

git checkout $DEPLOYMENT_BRANCH
git pull

sudo docker-compose down
sudo docker-compose up --build -d
