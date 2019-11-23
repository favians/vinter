ssh-add $TRAVIS_PROJECT_DIR/deployment/vinter.pem
ssh-keygen -R $DEVELOPMENT_HOST
ssh-keyscan -H $DEVELOPMENT_HOST >> ~/.ssh/known_hosts
ssh -v -i $TRAVIS_PROJECT_DIR/deployment/vinter.pem $DEVELOPMENT_SSH_USER@$DEVELOPMENT_HOST DEVELOPMENT_APP_PATH=$DEVELOPMENT_APP_PATH DEVELOPMENT_BRANCH=$DEVELOPMENT_BRANCH 'bash -s' < $TRAVIS_PROJECT_DIR/deployment/deploy-devel.sh
