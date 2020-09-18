from flask import request
from flask import make_response, jsonify
from project.server.managers.database import db
from project.server.models.ai_models import Models
from project.server.helpers.serialize import get_json_clean_response
from project.server.helpers import database

def select_all_models(restful):
    query = Models.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Models.model_name, Models.model_path, Models.dataset, Models.updated_on])
    query = query.order_by(*database.get_order_by(Models, restful.order_by))
    return database.get_list(query, restful.pagination)

def select_model(model_name):
    query = get_json_clean_response(Models.query.filter(Models.model_name == model_name))
    response_object = {
        'status': 'success',
        'data': query
    }
    return make_response(jsonify(response_object)), 200

def insert_models():
    post_data = request.get_json()
    db.session.bulk_insert_mappings(Models, post_data)
    db.session.commit()
    return {"Hello": 2}