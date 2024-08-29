 #!/bin/sh
ls -l secrets-output

# Debugging: Print the contents of the secrets file
echo "Contents of secrets.env:"
cat secrets-output/secrets.env

set -a
. secrets-output/secrets.env
set +a
ls secrets-output/secrets.env


cd python-script-repo
# Install necessary Python libraries

pip install --upgrade pip
pip install -r requirements.txt


# Run the Python script with environment variables
python test.py




