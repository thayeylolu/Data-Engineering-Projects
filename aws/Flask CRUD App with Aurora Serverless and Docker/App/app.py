# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import boto3
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('AWS_ACCESS_KEY_ID')

config = Config(region_name=os.getenv('AWS_REGION'))
rds_data = boto3.client(
    'rds-data',
    config=config,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

aurora_db_name = os.getenv('AURORA_DB_NAME')
aurora_cluster_arn = os.getenv('AURORA_CLUSTER_ARN')
aurora_secret_arn = os.getenv('AURORA_SECRET_ARN')


@app.route('/')
def Index():
    response = callDbWithStatement("SELECT * FROM users")
    recorder = []
    all_records = response['records']  # 2
    for user_info in range(len(all_records)):
        records = all_records[user_info]
        user = {'id': records[0]['longValue'], 'username': records[1]['stringValue'],
                'age': records[2]['longValue'], 'email': records[3]['stringValue']}
        recorder.append(user)
    list_user_tuple = [(d["id"], d["username"], d['age'], d['email']) for d in recorder]
    return render_template('index.html', list_users=list_user_tuple)


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        email = request.form['email']
        params = [
            {'name': 'username', 'value': {'stringValue': username}},
            {'name': 'age', 'value': {'longValue': int(age)}},
            {'name': 'email', 'value': {'stringValue': email}}
        ]

        callDbWithStatement("INSERT INTO users (username, age, email) VALUES (:username, :age, :email)", params=params)
        flash('User Added Successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_user(id):
    params = [{'name': 'id', 'value': {'longValue': int(id)}}]
    response = callDbWithStatement('SELECT * FROM users WHERE id =:id', params=params)
    records = response['records']

    user_info = [{'id': records[0][0]['longValue'],
        'username': records[0][1]['stringValue'],
         'age': int(records[0][2]['longValue']),
         'email': records[0][3]['stringValue']}]

    # return user_info # [{"age":34,"email":"demoo@gmail.com","username":"Vilinus"}]
    return render_template('edit.html', user=user_info[0])


@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        email = request.form['email']

        params = [
            {'name': 'username', 'value': {'stringValue': username}},
            {'name': 'age', 'value': {'longValue': int(age)}},
            {'name': 'email', 'value': {'stringValue': email}}
        ]

        callDbWithStatement(f"UPDATE users SET username = :username, age = :age, email = :email WHERE id = {id} ",
                            params=params)

        flash('User Updated Successfully')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_user(id):
    callDbWithStatement('DELETE FROM users WHERE id = {0}'.format(id))
    flash('User Deleted Successfully')
    return redirect(url_for('Index'))


def callDbWithStatement(sql, params=None):
    response = rds_data.execute_statement(
        database=aurora_db_name,
        resourceArn=aurora_cluster_arn,
        secretArn=aurora_secret_arn,
        sql=sql,
        parameters=params if params is not None else [],
        includeResultMetadata=True
    )
    print(f'Making Call... {sql}')
    print('-.-' * 20)
    print(response)
    return response


if __name__ == "__main__":
    app.run(debug=True)
