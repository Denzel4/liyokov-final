from flask import request
from project.server.managers.database import db
from project.server.models.sys_image import Image
from project.server.helpers import database

def insert_image():
    post_data = request.get_json()
    db.session.bulk_insert_mappings(Image, post_data)
    db.session.commit()

def select_image(restful):
    query = Image.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Image.area])
    query = query.order_by(*database.get_order_by(Image, restful.order_by))
    return database.get_list(query, restful.pagination)

def update_image(image_id):
    data = request.get_json()
    db.session.query(Image).filter_by(id=image_id).update(data)
    db.session.commit()

def drop_image(image_id):
    image = Image.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()