import json
import boto3
from botocore.exceptions import ClientError

def get_secret_api_key():
    secret_name = "prod/api/key/chatgpt"
    secret_key = "api-key-chatgpt"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret_response = get_secret_value_response[ 'SecretString' ]
    secret_object = json.loads(secret_response) 
    secret_api_key = secret_object['api-key-chatgpt']
    
    # Return secret
    return secret_api_key
    
def mask_value(str):
    newStr = ""
    for i in range(len(str)):
        if i <  7:
            newStr += str[i]
        else:
            newStr += '*'
    return newStr

def lambda_handler(event, context):
    api_key = get_secret_api_key()
    masked_api_key = mask_value( api_key )
    
    print( masked_api_key )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Successful Retreival of secret from AWS Secrets Manager')
    }