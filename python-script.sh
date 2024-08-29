#!/bin/sh


set -a
. secrets-output/secrets.env
set +a
ls secrets-output/secrets.env


cd python-script-repo
# Install necessary Python libraries
apt-get update
apt-get install -y wget
pip install --upgrade pip
pip install -r requirements.txt


# Run the Python script with environment variables
python test.py




