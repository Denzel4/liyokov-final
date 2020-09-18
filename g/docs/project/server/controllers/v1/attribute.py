from flask import request

from project.server.handlers.database.attribute import update_attribute, create_attribute, get_attribute, \
    get_attribute_list, delete_attribute


def create():
    return create_attribute()


def get(attribute_id):
    return get_attribute(attribute_id)


def get_list():
    return get_attribute_list(request.restful)


def update(attribute_id):
    return update_attribute(attribute_id)


def delete(attribute_id):
    return delete_attribute(attribute_id)
