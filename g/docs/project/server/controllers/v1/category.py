from flask import request

from project.server.handlers.database.category import create_category, get_category, get_category_list, update_category, \
    delete_category


def create():
    return create_category()


def get(category_id):
    return get_category(category_id)


def get_list():
    return get_category_list(request.restful)


def update(category_id):
    return update_category(category_id)


def delete(category_id):
    return delete_category(category_id)
