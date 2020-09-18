from project.server.helpers.serialize import get_json_clean_response
from flask import make_response, jsonify
from project.server.managers.database import db
from datetime import datetime
from project.server.models.ai_inference import Inference

def insert_inference():
    inference = Inference(
        updated_on=datetime.now(),
        agent_id=2,
        file_name='Image1',
        file_path='/home/ubuntu/Image1',
        tag='GOOD',
        model_id=1,
        camera_id=3,
        dataset='semi-conductor',
        confidence=1,
        label='GOOD'

    )
    db.session.add(inference)
    db.session.commit()
    response_object = {
        'status': 'success',
        'data': inference.to_dictionary()
    }
    return make_response(jsonify(response_object)), 200