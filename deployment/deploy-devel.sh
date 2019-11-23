cd $DEVELOPMENT_APP_PATH

git checkout master
git branch -D $DEVELOPMENT_BRANCH
git fetch origin
git checkout $DEVELOPMENT_BRANCH
git pull origin $DEVELOPMENT_BRANCH

sudo docker-compose down
sudo docker-compose up --build -d
