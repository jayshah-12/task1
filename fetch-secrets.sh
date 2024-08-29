
cd python-script-repo

echo "Vault Address: $VAULT_ADDR"
echo "Vault Token: $VAULT_TOKEN"

# Export environment variables
export VAULT_ADDR="$VAULT_ADDR"
export VAULT_TOKEN="$VAULT_TOKEN"

# Test connection to Vault
curl --header "X-Vault-Token: $VAULT_TOKEN" "$VAULT_ADDR/v1/sys/health"

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
