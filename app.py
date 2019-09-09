import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'sqlite:///' + os.path.join(basedir, 'db.rent_splitr')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to not mess with sqlite

db = SQLAlchemy(app)

marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000

#this is how you define a route
@app.route('/') 
def hello_world():
    return 'Hello World'

# ------------------------------------ GROUPS -------------------------------------------
@app.route('/group', methods=['GET', 'POST'])
@app.route('/group/<group_id>', methods=['GET', 'POST'])
def create_or_read_group(group_id=None):
    from models import Group
    if group_id == None and request.method == 'GET':
        return Group.get_groups()
    elif group_id == None:
        group_name = request.json['group_name']
        return Group.create_group(group_name)
    else:
        return Group.get_group(group_id)

@app.route('/group/<group_id>', methods=['PUT','DELETE'])
def destroy_or_modify_group(group_id):
    from models import Group
    if request.method == 'PUT':
        return Group.update_group(group_id)
    else:
        return Group.delete_group(group_id)

# ------------------------------------ MEMBERS -------------------------------------------
@app.route('/member', methods=['POST', 'GET'])
@app.route('/member/<member_id>', methods=['GET'])
def get_or_create_member(member_id=None):
    from models import Member
    if member_id == None and request.method == 'GET':
        return Member.get_members()
    elif member_id == None:
        name = request.json['name']
        email = request.json['email']
        acct_receivable = request.json['acct_receivable']
        acct_payable = request.json['acct_payable']
        return Member.create_member(name, email, acct_receivable, acct_payable,)
    else:
        return Member.get_member(member_id)

@app.route('/member/<member_id>', methods=['PUT', 'DELETE'])
def update_or_delete_member(member_id=None):
    from models import Member
    if request.method == 'PUT':
        req = request.get_json()
        return Member.update_member(member_id, **req)
    else:
        return Member.delete_member(member_id)

# ------------------------------------ EXPENSES -------------------------------------------

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)