from flask import request
from project.server.handlers.database.annotation import update_annotation, create_annotation, get_annotation, \
    get_annotation_list, delete_annotation


def create():
    return create_annotation()


def get(annotation_id):
    return get_annotation(annotation_id)


def get_list():
    return get_annotation_list(request.restful)


def update(annotation_id):
    return update_annotation(annotation_id)


def delete(annotation_id):
    return delete_annotation(annotation_id)
