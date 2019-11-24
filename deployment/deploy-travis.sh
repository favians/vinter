ssh-add $TRAVIS_PROJECT_DIR/deployment/vinter.pem
ssh-keygen -R $DEPLOYMENT_HOST
ssh-keyscan -H $DEPLOYMENT_HOST >> ~/.ssh/known_hosts
ssh -v -i $TRAVIS_PROJECT_DIR/deployment/vinter.pem $DEPLOYMENT_SSH_USER@$DEPLOYMENT_HOST DEPLOYMENT_APP_PATH=$DEPLOYMENT_APP_PATH DEPLOYMENT_BRANCH=$DEPLOYMENT_BRANCH 'bash -s' < $TRAVIS_PROJECT_DIR/deployment/deployment.sh
