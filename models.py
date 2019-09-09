from app import db, marshmallow
from flask import jsonify, request
# from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

# ------------------------------------ GROUPS -------------------------------------------
class Group(db.Model):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), unique=True)

    def __init__(self, group_name):
        self.group_name = group_name
    
    @classmethod
    def create_group(cls, group_name):
        new_group = Group(group_name)
        try:
            db.session.add(new_group)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return group_schema.jsonify(new_group)
    @classmethod
    def get_group(cls, group_id):
        group = Group.query.get(group_id)
        return group_schema.jsonify(group)
    @classmethod
    def get_groups(cls):
        groups = Group.query.all()
        return groups_schema.jsonify(groups)
    @classmethod
    def delete_group(cls, group_id):
        group = Group.query.get(group_id)
        db.session.delete(group)
        db.session.commit
        return group_schema.jsonify(group)
    @classmethod
    def update_group(cls, group_id):
        group = Group.query.get(group_id)
        group_name = request.json['group_name']
        group.group_name = group_name
        db.session.commit()
        return group_schema.jsonify(group)

class GroupSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'group_name')

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

# ------------------------------------ MEMBERS -------------------------------------------
class Members(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    acct_payable = db.Column(db.Integer)
    acct_receivable = db.Column(db.Integer)
    group = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, name, email, acct_receivable, acct_payable, group):
        self.name = name
        self.email = email
        self.acct_receivable = acct_receivable
        self.acct_payable = acct_payable
        self.group = group
    
    @classmethod
    def create_member(cls, name, email, acct_receivable, acct_payable, group):
        new_member = Member(name, email, acct_receivable, acct_payable, group)
        try: 
            db.session.add(new_member)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return member_schema.jsonify(new_member)
    @classmethod
    def get_member(cls, member_id):
        member = Member.query.get(member_id)
        return member_schema.jsonify(member)
    @classmethod
    def get_members(cls):
        members = Member.query.all()
        return members_schema.jsonify(members)
    @classmethod
    def delete_member(cls, member_id):
        member = Member.query.get(member_id)
        db.session.delete(member)
        db.session.commit
        return member_schema.jsonify(member)
    @classmethod
    def update_comment(cls, member_id, name=None, email=None, acct_receivable=None, acct_payable=None):
        member = Member.query.get(member_id)
        if name != None:
            member.name = name 
        if email != None:
            member.email = email 
        if acct_receivable != None:
            member.acct_receivable = acct_receivable 
        if acct_payable != None:
            member.acct_payable = acct_payable
        db.session.commit()
        return member_schema.jsonify(member)

class MemberSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'acct_receivable', 'acct_payable' )

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)



if __name__ == 'models':
    db.create_all()