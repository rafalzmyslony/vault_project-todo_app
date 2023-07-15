import os
import hvac

# Initialize the Vault client
client = hvac.Client()

# Configure the Vault client with the appropriate authentication method
client.auth.aws_ec2_role(role='vault-role-for-aws-ec2role')

# Fetch the password from Vault
result = client.secrets.kv.v2.read_secret_version(path='kv/db/todo_app')

# Extract the password from the response
password = result['data']['data']['password']

# Set the password as an environment variable
os.environ['DB_PASSWORD'] = password

# Print the password to verify
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")