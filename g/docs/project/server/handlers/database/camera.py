from datetime import datetime
from flask import jsonify, request, make_response
from project.server.helpers.serialize import get_json_clean_response
from project.server.managers.database import db
from project.server.models.sys_camera import Camera
from project.server.helpers import database



def insert_preset():
    # get the post data
    post_data = request.get_json()
    camera = Camera(
        camera_id=post_data.get('camera_id'),
        updated_on=datetime.now(),
        camera_type=post_data.get('camera_type'),
        frame_rate=post_data.get('frame_rate'),
        resolution=post_data.get('resolution'),
        color=post_data.get('color'),
        shutter_speed=post_data.get('shutter_speed'),
        exposure=post_data.get('exposure'),
        image_size_H=post_data.get('image_size_H'),
        image_size_W=post_data.get('image_size_W'),
        image_size_C=post_data.get('image_size_C'),
        spot_name=post_data.get('spot_name'),
        weight_file=post_data.get('weight_file'),
        threshold=post_data.get('threshold'),
        orientation=post_data.get('orientation'),

    )
    db.session.add(camera)
    db.session.commit()
    return "Test"


def select_all_camera(restful):
    query = Camera.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q,
                                      [Camera.camera_id])
    query = query.order_by(*database.get_order_by(Camera, restful.order_by))
    # query = get_json_clean_response(Models.query.all())
    return database.get_list(query, restful.pagination)