from flask import request

from project.server.controllers.v1 import errors
from project.server.managers.database import db
from project.server.models.ai_category import Category
from project.server.helpers import database


def create_category():
    data = request.get_json()
    db.session.bulk_insert_mappings(Category, data)
    db.session.commit()


def get_category(category_id):
    try:
        dataset = Category.query.get_or_404(category_id)
        return dataset.to_dictionary()
    except Exception as e:
        print(e)
        return errors.not_found(message='not_found')


def get_category_list(restful):
    query = Category.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Category.category_name])
    query = query.order_by(*database.get_order_by(Category, restful.order_by))
    return database.get_list(query, restful.pagination)


def update_category(category_id):
    data = request.get_json()
    db.session.query(Category).filter_by(category_id=category_id).update(data)
    db.session.commit()


def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
