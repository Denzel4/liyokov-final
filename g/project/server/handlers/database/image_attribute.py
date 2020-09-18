from flask import request
from project.server.managers.database import db
from project.server.models.sys_image import Image
from project.server.helpers import database
from project.server.handlers.filesystem.dataset import rename_dataset
from project.server import app

def select_all_attributes(restful):
    query = Image.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q,
                                      [Image.flagging])
    query = query.order_by(*database.get_order_by(Image, restful.order_by))
    return database.get_list(query, restful.pagination)

def update_all_attributes():
    data = request.get_json()
    db.session.query(Image).filter_by(agent_id=7).update(data)
    db.session.commit()
    return {
        "data": "query1.to_dictionary()"
    }

def select_by_dataset():
    request_data = request.get_json()
    output_data = db.session.query(Image).filter_by(dataset=request_data['dataset']).all()
    return output_data

def delete_by_dataset():
    request_data = request.get_json()
    db.session.query(Image).filter_by(dataset=request_data['dataset']).delete()
    db.session.commit()
    return {
        "status": f"All Image Attribute with {request_data['dataset']} have been removed."
    }

def update_by_dataset():
    request_data = request.get_json()
    dataset_updated = request_data['dataset']
    request_data.pop('dataset', None)
    db.session.query(Image).filter_by(dataset=dataset_updated).update(request_data)
    db.session.commit()
    return {
        "status": f"All Image Attribute with {dataset_updated} have been updated new values."
    }

def insert_image_attribute():
    request_data = request.get_json()
    new_image_attribute = Image()
    new_image_attribute.from_json(request_data)
    if request_data.get("image_path", None) is not None:
        new_image_attribute.image_path = request_data['image_path']
    db.session.add(new_image_attribute)
    db.session.commit()
    return {
        "status": f"New Image Attribute with info {new_image_attribute.to_dictionary()} has been inserted."
    }

def update_dataset(dataset_name):
    data = request.get_json()
    try:
        rename_dataset(dataset_name, data.get('dataset_name'))
        db.session.query(Image).filter_by(dataset=dataset_name).update(data.get(dataset_name))
        db.session.commit()
    except FileExistsError:
        pass
    return "Dataset has been updated"

