import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite Database
DATABASE = 'sqlite:///' + os.path.join(basedir, 'db.rent_splitr')

# Local Postgres Database
# DATABASE = 'postgresql://localhost/reddit'
# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to not mess with sqlite

# Init Database
db = SQLAlchemy(app)

#Init Marshmallow - schemas and json
marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000

#this is how you define a route
@app.route('/') 
def hello_world():
    return 'Hello World'

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
def destroy_or_modify(group_id):
    from models import Group
    if request.method == 'PUT':
        return Group.update_group(group_id)
    else:
        return Group.delete_group(group_id)



@app.route('/group/<group_id>', methods=['PUT','DELETE'])
def destroy_or_modify(group_id):
    from models import Group
    if request.method == 'PUT':
        return Group.update_group(group_id)
    else:
        return Group.delete_group(group_id)


# @app.route('/group/<group_id>', methods=['DELETE'])
# def destroy_group(group_id):
#     from models import Group
#     return Group.delete_group(group_id)

# @app.route('/group/<group_id>', methods=['PUT'])
# def modify_group(group_id):
#     from models import Group
#     return Group.update_group(group_id)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)