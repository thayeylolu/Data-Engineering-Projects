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
        userid SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        user_email VARCHAR(50) UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );'''
    return create_table_command


# get a user by id
@app.route('/getUser')
def getUser():
    id = request.args.get('userid')
    response = callDbWithStatement("SELECT * FROM users WHERE id ='" + str(id) + "'")
    user = {}
    records = response['records']
    for record in records:
        user['userid'] = record[0]['longValue']
        user['username'] = record[1]['stringValue']
        user['user_email'] = record[2]['stringValue']
        user['age'] = record[3]['longValue']
        user['date_created'] = record[4]['stringValue']
    print(user)
    return jsonify(user)


# get all users
@app.route('/AllUser')
def getAllUser():
    response = callDbWithStatement("SELECT * FROM users")
    recorder = {}
    all_records = response['records']  # 2
    for user_info in range(len(all_records)):
        records = all_records[user_info]
        user = {'userid': records[0]['longValue'], 'username': records[1]['stringValue'],
                'user_email': records[2]['stringValue'], 'age': records[3]['longValue'],
                'date_created': records[4]['stringValue']}
        recorder[int(user['userid'])] = user

    print('*' * 30)
    print(recorder)
    print('*' * 30)
    return jsonify(recorder)


# create users
@app.route('/createUser', methods=['POST'])
def createUser():
    request_data = request.get_json()
    usr_id = request_data['userid']
    usr_name = request_data['username']
    usr_email = request_data['user_email']
    age = request_data['age']
    date_created = request_data['date_created']

    callDbWithStatement("INSERT INTO users (userid, username, user_email, age, date_created) VALUES ('"
                        + str(usr_id) + "', '" + usr_name + "', '" + usr_email + "','" + str(age) + "','" + date_created + "');")
    return "Done"


# update users
@app.route('/updateUser', methods=['POST'])
def UpdateUser():
    email = request.json['user_email']
    response = callDbWithStatement("SELECT * FROM users WHERE user_email='" + email + "';")
    new_data = request.json['new_data']
    callDbWithStatement('UPDATE users SET name=?, age=?, city=? WHERE email=?',
                       (new_data['name'], new_data['age'], new_data['city'], email))



def callDbWithStatement(sql):
    response = rds_data.execute_statement(
        database=aurora_db_name,
        resourceArn=aurora_cluster_arn,
        secretArn=aurora_secret_arn,
        sql=sql,
        includeResultMetadata=True
    )
    print(f'Making Call... {sql}')
    print('.-' * 20)
    print(response)
    return response


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8081)
