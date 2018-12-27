#!/bin/bash

ROLE_DIR="aws_alias_role"

echo "To carry out these tests, kindly ensure you have GIT, DOCKER, RUBY(=2.3.1) and BUNDLER, PYTHON, PIP installed on your machine"
echo "pausing for 7 seconds"
sleep 7

echo "Setting up AWS ENV variables"
export AWS_STATE="present"
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# add functionality to enable continuing or exiting to install dependencies

cd $ROLE_DIR

echo "installing dependencies"
pip install -r requirements.txt

echo "installing ansible==2.0"
pip install ansible==2.0
echo "RUNNING TESTS FOR Ansible V2.0"
nosetests -v library/
echo "pausing for 5 seconds"
sleep 3

echo "installing ansible==2.1"
pip install ansible==2.1
echo "RUNNING TESTS FOR Ansible V2.1"
nosetests -v library/
echo "pausing for 5 seconds"
sleep 3

echo "installing ansible==2.2"
pip install ansible==2.2.1.0
echo "RUNNING TESTS FOR Ansible V2.2"
nosetests -v library/
echo "pausing for 5 seconds"
sleep 3

echo "Installing integration test dependencies"
sudo bundle install

echo "performing integration tests"
kitchen test
