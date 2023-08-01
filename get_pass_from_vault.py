import boto3
import hvac
import os
import time
'''
Script prints password from HCP Vault kept in this path: kv/data/db/todo_app from field password (kv/data/db/todo_app/password

'''
def get_pass_vault():
    _todo_env_location = 'todo_env'
    _VAULT_ADDRESS = os.getenv('VAULT_ADDR')
    MAX_RETRIES = 5
    RETRY_DELAY = 1  # seconds

    def connect_to_vault():
        # get credentials from EC2 metadata (vault is auth via IAM role)
        session = boto3.Session()
        credentials = session.get_credentials()
        try:
            client = hvac.Client(url=_VAULT_ADDRESS)
            client.auth.aws.iam_login(credentials.access_key, credentials.secret_key, credentials.token, role='vault-role-for-aws-ec2role')
            return client
        except:
            #print(f"Error connecting to Vault: {e}")
            return None

    # Get the client object with retries
    client = None
    retry_count = 0

    while retry_count < MAX_RETRIES:
        client = connect_to_vault()
        if client:
            #it breaks while loop
            break

        retry_count += 1
        print(f"Retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)

    # If the client is still None after retries, raise an error or handle it accordingly
    if not client:
        #raise Exception("Failed to connect to Vault after multiple retries.")
        return False

    # Fetch the secret data from Vault
    mount_point = 'kv'
    secret_path = 'db/todo_app'

    read_secret_result = client.secrets.kv.v2.read_secret(
        path=secret_path,
        mount_point=mount_point
    )
    password = read_secret_result['data']['password']
    #print(password)
    # replace password in todo_env file on current from HCP vault
    with open(_todo_env_location, "r") as f1:
        lines = f1.readlines()

    for i, line in enumerate(lines):
        if 'DB_PASSWORD' in line:
            lines[i] = 'DB_PASSWORD='+format(password)+'\n'
            with open(_todo_env_location, "w") as f:
                f.writelines(lines)
            f.close()
    f1.close()
    return True
