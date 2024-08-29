
cd python-script-repo
# Set Vault address and token
export VAULT_ADDR=${VAULT_ADDR}
export VAULT_TOKEN=${VAULT_TOKEN}


echo "VAULT_ADDR=${{ secrets.VAULT_ADDR }}" >> $GITHUB_ENV
echo "VAULT_TOKEN=${{ secrets.VAULT_TOKEN }}" >> $GITHUB_ENV
# echo "VAULT_SECRET=${{ secrets.VAULT_SECRET }}" >> $GITHUB_ENV


if [ -z "$VAULT_ADDR" ]; then
  echo "Error: VAULT_ADDR is not set."
  exit 1
fi

if [ -z "$VAULT_TOKEN" ]; then
  echo "Error: VAULT_TOKEN is not set."
  exit 1
fi

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
