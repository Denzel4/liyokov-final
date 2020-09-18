from datetime import datetime

from project.server.helpers.serialize import get_json_clean_response
from project.server.managers.database import db
from project.server.models.ai_annotation import Annotation
from project.server.models.ai_attribute import Attribute
from project.server.models.ai_category import Category
from project.server.models.ai_dataset import Dataset


class Image(db.Model):
    """ Image Model for storing image related details """
    __tablename__ = 'sys_image'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    updated_on = db.Column(db.DateTime, nullable=True, default=datetime.now())
    image_path = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('ai_dataset.id', ondelete='CASCADE', onupdate="cascade"),
                           nullable=True)
    attributes_id = db.Column(db.Integer, db.ForeignKey('ai_attribute.id', ondelete='CASCADE'), nullable=True, default=1)
    annotation_id = db.Column(db.Integer, db.ForeignKey('ai_annotation.id', ondelete='CASCADE'), nullable=True, default=1)
    categories_id = db.Column(db.Integer, db.ForeignKey('ai_category.id', ondelete='CASCADE'), nullable=True, default=1)
    annotation_path = db.Column(db.String(255), nullable=True, default='NULL')
    flagging = db.Column(db.String(255), nullable=True, default='NULL')
    license = db.Column(db.String(255), nullable=True, default='NULL')
    width = db.Column(db.Float, nullable=True, default='1')
    height = db.Column(db.Float, nullable=True, default='1')
    dataset = db.relationship(Dataset, primaryjoin=dataset_id == Dataset.id, post_update=True)
    attribute = db.relationship(Attribute, primaryjoin=attributes_id == Attribute.id, post_update=True)
    category = db.relationship(Category, primaryjoin=categories_id == Category.id, post_update=True)
    annotation = db.relationship(Annotation, primaryjoin=annotation_id == Annotation.id, post_update=True, uselist=True)

    def __init__(self, updated_on, image_path, filename, dataset_id,
                 attributes_id=None, categories_id=None, annotation_id=None):
        self.updated_on = updated_on
        self.image_path = image_path
        self.filename = filename
        if dataset_id is not None:
            self.dataset = Dataset.query.get_or_404(dataset_id)
        if attributes_id is not None:
            self.attribute = Attribute.query.get_or_404(attributes_id)
        if annotation_id is not None:
            self.annotation = Annotation.query.get_or_404(annotation_id)
        if categories_id is not None:
            self.category = Category.query.get_or_404(categories_id)


    def from_json(self, json):
        self.id = json.get('image_id', None)
        self.updated_on = json.get('updated_on', None)
        self.image_path = json.get('image_path', None)
        self.dataset = json.get('dataset', None)
        return self

    def to_dictionary(self):
        obj = {
            'image_id': self.id,
            'updated_on': self.updated_on,
            'image_path': self.image_path,
            'filename': self.filename,
            'dataset_id': self.dataset_id,
            # 'agent': [get_json_clean_response(self.agent)],
            'annotation': get_json_clean_response(self.annotation),
            'attributes': [get_json_clean_response(self.attribute)],
            'categories': [get_json_clean_response(self.category)]
        }
        return obj
