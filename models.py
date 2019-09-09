from app import db, marshmallow
from flask import jsonify, request
# from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)


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








if __name__ == 'models':
    db.create_all()