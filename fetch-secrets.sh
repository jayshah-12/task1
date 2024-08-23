

# Set Vault address and token
export VAULT_ADDR='http://192.168.3.112:8200'
export VAULT_TOKEN='root'

# Fetch secrets from Vault
username=$(vault kv get -field=username secret/myapp)
password=$(vault kv get -field=password secret/myapp)

# Store secrets in a file
mkdir -p secrets-output  # Ensure the directory exists
echo "USERNAME=$username" > secrets-output/secrets.env
echo "PASSWORD=$password" >> secrets-output/secrets.env

# Set proper file permissions (e.g., read and write only for the owner)
chmod 600 secrets-output/secrets.env

# Debugging: List the contents of the secrets directory
echo "Contents of secrets-output directory:"
ls -l secrets-output

# Debugging: Print the contents of the secrets file
echo "Contents of secrets.env:"
cat secrets-output/secrets.env
