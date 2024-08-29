
cd python-script-repo

echo "Vault Address: $VAULT_ADDR"
echo "Vault Token: $VAULT_TOKEN"

# Check if environment variables are set
if [ -z "$VAULT_ADDR" ] || [ -z "$VAULT_TOKEN" ]; then
    echo "Error: VAULT_ADDR or VAULT_TOKEN is not set."
    exit 1
fi

# Export environment variables
export VAULT_ADDR="$VAULT_ADDR"
export VAULT_TOKEN="$VAULT_TOKEN"

# Test connection to Vault
curl --header "X-Vault-Token: $VAULT_TOKEN" "$VAULT_ADDR/v1/sys/health


# Fetch secrets from Vault
username=$(vault kv get -field=username secret/myapp)
password=$(vault kv get -field=password secret/myapp)

# Store secrets in a file
mkdir -p secrets-output  # Ensure the directory exists
echo "USERNAME=$username" > secrets-output/secrets.env
echo "PASSWORD=$password" >> secrets-output/secrets.env

chmod 600 secrets-output/secrets.env


echo "Contents of secrets-output directory:"
ls -l secrets-output

# Debugging: Print the contents of the secrets file
echo "Contents of secrets.env:"
cat secrets-output/secrets.env
