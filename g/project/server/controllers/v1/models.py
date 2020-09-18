from flask import request
from project.server.handlers.database.models import select_all_models, insert_models

def get_models():
    return select_all_models(request.restful)

def insert_model():
    return insert_models()
