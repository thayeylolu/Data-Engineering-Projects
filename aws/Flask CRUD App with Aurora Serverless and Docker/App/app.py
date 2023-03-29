from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# initialize flask app
app = Flask(__name__)

# get database url

# config = Config(region_name=os.getenv('AWS_REGION'))
# rds_data = boto3.client(
#     'rds-data',
#     config=config,
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
#
# aurora_db_name = os.getenv('AURORA_DB_NAME')
# aurora_cluster_arn = os.getenv('AURORA_CLUSTER_ARN')
# aurora_secret_arn = os.getenv('AURORA_SECRET_ARN')

# connect DB endpoint
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('AURORA_DB_URL')
db = SQLAlchemy(app)


# User Schema Class
class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    # date_created = ...


# initialize class objects
def __init__(self, username, email, age):
    self.username = username
    self.email = email
    self.age = age


# create DB
db.create_all()


# get user by id endpoint
@app.route('/users/<userid>', methods=['GET'])
def get_user(userid):
    user = User.query.get(userid)
    del user.__dict__['_sa_instance_state']
    return jsonify(user.__dict__)


# get all users endpoint
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in db.session.query(User).all():
        del user.__dict__['_sa_instance_state']
        users.append(user.__dict__)
    return jsonify(users)


# create user endpoint
@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    db.session.add(User(body['username'], body['email'], body['age']))
    db.session.commit()
    return "user created"


# update user endpoint
@app.route('/users/<id>', methods=['PUT'])
def update_user(userid):
    body = request.get_json()
    db.session.query(User).filter_by(id=userid).update(
        dict(email=body['email'], username=body['username'], age=body['age']))
    db.session.commit()
    return "User Details updated"


# delete user by email
@app.route('/users/<email>', methods=['DELETE'])
def delete_item(email):
    db.session.query(User).filter_by(id=email).delete()
    db.session.commit()
    return "User profile deleted"


if __name__ == '__main__':
    app.run(debug=True)
