from flask import request

from project.server.controllers.v1 import errors
from project.server.managers.database import db
from project.server.helpers import database
from project.server.models import Annotation


def create_annotation():
    data = request.get_json()
    db.session.bulk_insert_mappings(Annotation, data)
    db.session.commit()


def get_annotation(annotation_id):
    try:
        annotation = Annotation.query.get_or_404(annotation_id)
        return annotation.to_dictionary()
    except Exception as e:
        print(e)
        return errors.not_found(message='not_found')


def get_annotation_list(restful):
    query = Annotation.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Annotation.annotation_name])
    query = query.order_by(*database.get_order_by(Annotation, restful.order_by))
    return database.get_list(query, restful.pagination)


def update_annotation(annotation_id):
    data = request.get_json()
    db.session.query(Annotation).filter_by(annotation_id=annotation_id).update(data)
    db.session.commit()


def delete_annotation(annotation_id):
    annotation = Annotation.query.get_or_404(annotation_id)
    db.session.delete(annotation)
    db.session.commit()
