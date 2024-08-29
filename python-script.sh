 #!/bin/sh
cd python-script-repo
# Install necessary Python libraries
apt-get update
apt-get install -y wget
pip install --upgrade pip
pip install -r requirements.txt

cd ..
# Source the environment variables from the secrets file
set -a
. secrets-output/secrets.env
set +a
ls secrets-output/secrets.env
# Change directory to where the Python script is located
cd python-script-repo

# Run the Python script with environment variables
python test.py




