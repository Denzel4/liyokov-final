import datetime

from project.server.helpers.encrypter import encrypt_password
from project.server.managers.database import db


class Models(db.Model):
    """ Models Model for storing model related details """
    __tablename__ = "ai_models"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_on = db.Column(db.DateTime(), nullable=True)
    model_name = db.Column(db.String(255), nullable=True)
    model_path = db.Column(db.String(255), nullable=True)
    camera_id = db.Column(db.String(255), nullable=True)
    dataset = db.Column(db.String(255), nullable=True)

    def __init__(self, updated_on, model_name, model_path, camera_id, dataset):
        self.model_name = model_name
        self.updated_on = updated_on
        self.model_path = model_path
        self.camera_id = camera_id
        self.dataset = dataset

    def from_json(self, json):
        self.id = json.get('user_id', None)
        self.updated_on = json.get('updated_on', None)
        self.model_name = json.get('model_name', None)
        self.model_path = json.get('model_path', None)
        self.camera_id = json.get('camera_id', None)
        self.dataset = json.get('dataset', None)
        return self

    def to_dictionary(self):
        obj = {
            'model_id': self.id,
            'model_name': self.model_name,
            'updated_on': self.updated_on,
            'model_path': self.model_path,
            'camera_id': self.camera_id,
            'dataset': self.dataset
        }
        return obj
