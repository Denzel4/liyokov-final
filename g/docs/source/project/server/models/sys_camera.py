from datetime import datetime
from project.server.managers.database import db
from project.server.models.ai_models import Models
from project.server.models.ai_inference import Inference
from project.server.helpers.serialize import get_json_clean_response
from project.server.models.ai_agent import Agent
from project.server.models.ai_models import Models
from project.server.models.ai_inference import Inference


class Camera(db.Model):
    """ Camera Model for storing camera related details """
    __tablename__ = 'sys_camera'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    camera_id = db.Column(db.String(255), nullable=True)
    updated_on = db.Column(db.DateTime(), nullable=True)
    camera_type = db.Column(db.String(255), nullable=True)
    frame_rate = db.Column(db.String(255), nullable=True)
    resolution = db.Column(db.Float, nullable=True)
    color = db.Column(db.String(255), nullable=True)
    shutter_speed = db.Column(db.Boolean, nullable=True)
    exposure = db.Column(db.String(255), nullable=True)
    image_size_H = db.Column(db.Boolean, nullable=True)
    image_size_W = db.Column(db.String(255), nullable=True)
    image_size_C = db.Column(db.String(255), nullable=True)
    spot_name = db.Column(db.String(255), nullable=True)
    weight_file = db.Column(db.String(255), nullable=True)
    threshold = db.Column(db.String(255), nullable=True)
    orientation = db.Column(db.String(255), nullable=True)
    current_status = db.Column(db.Boolean, nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey("ai_agent.id", ondelete='CASCADE'), nullable=True)
    models_id = db.Column(db.Integer, db.ForeignKey("ai_models.id", ondelete='CASCADE'), nullable=True)
    agent = db.relationship(Agent, primaryjoin=agent_id == Agent.id)
    model = db.relationship(Models, primaryjoin=models_id == Models.id)
    # inference_id = db.Column(db.Integer, db.ForeignKey("ai_inference.id"), nullable=True)
    # inference = db.relationship(Inference, primaryjoin=inference_id == Inference.id)


    def __init__(self, camera_id, updated_on, camera_type, frame_rate, resolution, color, shutter_speed, exposure,
                 image_size_H,
                 image_size_W, image_size_C, spot_name, weight_file, threshold, orientation):
        self.camera_id = camera_id
        self.updated_on = updated_on
        self.camera_type = camera_type
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.color = color
        self.shutter_speed = shutter_speed
        self.exposure = exposure
        self.image_size_H = image_size_H
        self.image_size_W = image_size_W
        self.image_size_C = image_size_C
        self.spot_name = spot_name
        self.weight_file = weight_file
        self.threshold = threshold
        self.orientation = orientation
        self.model = Models.query.all()
        # self.inference = Inference.query.all()

    def from_json(self, json):
        self.camera_id = json.get('camera_id', None)
        self.updated_on = json.get('updated_on', None)
        self.camera_type = json.get('camera_type', None)
        self.frame_rate = json.get('frame_rate', None)
        self.resolution = json.get('resolution', None)
        self.color = json.get('color', None)
        self.shutter_speed = json.get('shutter_speed', None)
        self.exposure = json.get('exposure', None)
        self.image_size_H = json.get('image_size_H', None)
        self.image_size_W = json.get('image_size_W', None)
        self.image_size_C = json.get('image_size_C', None)
        self.spot_name = json.get('spot_name', None)
        self.weight_file = json.get('weight_file', None)
        self.threshold = json.get('threshold', None)
        self.orientation = json.get('orientation', None)

        return self

    def to_dictionary(self):
        obj = {
            'camera_id': self.camera_id,
            'updated_on': self.updated_on,
            'camera_type': self.camera_type,
            'frame_rate': self.frame_rate,
            'resolution': self.resolution,
            'color': self.color,
            'shutter_speed': self.shutter_speed,
            'exposure': self.exposure,
            'image_size_H': self.image_size_H,
            'image_size_W': self.image_size_W,
            'image_size_C': self.image_size_C,
            'weight_file': self.weight_file,
            'threshold': self.threshold,
            'orientation': self.orientation,
            'model': [get_json_clean_response(self.model)],
            # 'inference': [get_json_clean_response(self.inference)]
        }
        return obj
