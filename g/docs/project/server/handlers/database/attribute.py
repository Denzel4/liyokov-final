from flask import request

from project.server.controllers.v1 import errors
from project.server.managers.database import db
from project.server.models.ai_attribute import Attribute
from project.server.helpers import database


def create_attribute():
    data = request.get_json()
    db.session.bulk_insert_mappings(Attribute, data)
    db.session.commit()


def get_attribute(attribute_id):
    try:
        attribute = Attribute.query.get_or_404(attribute_id)
        return attribute.to_dictionary()
    except Exception as e:
        print(e)
        return errors.not_found(message='not_found')


def get_attribute_list(restful):
    query = Attribute.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Attribute.attribute_name])
    query = query.order_by(*database.get_order_by(Attribute, restful.order_by))
    return database.get_list(query, restful.pagination)


def update_attribute(attribute_id):
    data = request.get_json()
    db.session.query(Attribute).filter_by(attribute_id=attribute_id).update(data)
    db.session.commit()


def delete_attribute(attribute_id):
    attribute = Attribute.query.get_or_404(attribute_id)
    db.session.delete(attribute)
    db.session.commit()
