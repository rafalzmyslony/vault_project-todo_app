import boto3
import hvac
import os

'''
Script prints password from HCP Vault kept in this path: kv/data/db/todo_app from field password (kv/data/db/todo_app/password

'''
_VAULT_ADDRESS = os.getenv('VAULT_ADDR')

# get credentials from EC2 metadata (vault is auth via IAM role)
session = boto3.Session()
credentials = session.get_credentials()


client = hvac.Client(url=_VAULT_ADDRESS)
client.auth.aws.iam_login(credentials.access_key, credentials.secret_key, credentials.token, role='vault-role-for-aws-ec2role')
# Fetch the secret data from Vault
mount_point = 'kv'
secret_path = 'db/todo_app'

read_secret_result = client.secrets.kv.v2.read_secret(
    path=secret_path,
    mount_point=mount_point
)

print(read_secret_result['data']['data']['password'])                                                       
