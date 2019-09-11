import os

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'sqlite:///' + os.path.join(basedir, 'db.rent_splitr')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000

@app.route("/")
def expense():
    from models import Expenses
    expenses = Expenses.query.all()
    # print(expenses.description())
    print(expenses)
    return render_template('expenses.html', expenses=expenses)

@app.route("/add_expense", methods=("POST",))
def add_expense():
    from models import Expenses
    if request.method == "POST":
        Expenses.create_expense(
            description = request.form["description"],
            amount = request.form["amount"],
            member = request.form["member"]
        )
    return redirect(url_for('expense'))

# New route that is will delete entries
@app.route('/delete_expense/<id>', methods=("GET",))
def delete_expense(id):
    from models import Expenses
    if request.method == 'GET':
        Expenses.delete_expense(id)
    return redirect(url_for('expense')) 

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
        group = request.json['group']
        return Member.create_member(name, email, acct_receivable, acct_payable, group)
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
@app.route('/expenses', methods=['POST', 'GET'])
@app.route('/expenses/<expenses_id>', methods=['GET'])
def get_or_create_expenses(expenses_id=None):
    from models import Expenses
    if expenses_id == None and request.method == 'GET':
        return Expenses.get_expenses()
    elif expenses_id == None:
        description = request.json['description']
        amount = request.json['amount']
        member = request.json['member']
        return Expenses.create_expense(description, amount, member)
    else:
        return Expenses.get_expense(expenses_id)

@app.route('/expenses/<expenses_id>', methods=['PUT',])
def update_or_delete_expenses(expenses_id=None):
    from models import Expenses
    if request.method == 'PUT':
        description = request.json['description']
        amount = request.json['amount']
        Expenses.update_expenses(expenses_id, description, amount)
        return redirect(url_for('expense')) 

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)