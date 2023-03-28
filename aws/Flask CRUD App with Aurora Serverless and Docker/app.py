import os
from dotenv import load_dotenv
import boto3
from flask import Flask, jsonify, request
from botocore.config import Config

# Load the values from the .env file into the environment variables
load_dotenv()
app = Flask(__name__)

config = Config(region_name=os.getenv('AWS_REGION'))
rds_data = boto3.client(
    'rds-data',
    config=config,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

aurora_db_name = os.getenv('AURORA_DB_NAME')
aurora_cluster_arn = os.getenv('AURORA_CLUSTER_ARN')
aurora_secret_arn = os.getenv('AURORA_SECRET_ARN')


def create_usr_acct_tbl():
    create_table_command = '''CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        user_email VARCHAR(50) UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );'''
    return create_table_command

@app.route('/getUser'):
def getUser():
    id = request.args.get(id)
    response = callDbWithStatement("SELECT * FROM users WHERE id = '"+str(id)+"' ;")
    user = {}
    records = response['records']
    for record in records:
        user['id'] = record[0]['longValue']
        user['username'] = record[1]['stringValue']
        user['age'] = record[2]['stringValue']
        user['date_created'] = record[3]['stringValue']
    print(user)
    return jsonify(user)




if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8081)
