#!/bin/sh

# Install necessary Python libraries
apt-get update
apt-get install -y wget
pip install --upgrade pip
pip install requests pandas beautifulsoup4 mysql-connector-python sqlalchemy

# Source the environment variables from the secrets file
set -a
. secrets-output/secrets.env
set +a
ls secrets-output/secrets.env
# Change directory to where the Python script is located
cd python-script-repo

# Run the Python script with environment variables
python scrape3.py

# Create the output directory if it doesn't exist
# mkdir -p script-output

# # Move the resulting CSV to the output directory
# mv profit_and_loss.csv script-output/

# # Debugging: List the contents of the output directory
# echo "Contents of script-output directory:"
# ls -l script-output
