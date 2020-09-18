from project.server.managers.database import db


class Attribute(db.Model):
    """ Models Model for storing model related details """
    __tablename__ = "ai_attribute"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_on = db.Column(db.DateTime(), nullable=False)
    attribute_name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    dataset = db.Column(db.Integer,  nullable=False)

    def __init__(self, updated_on, attribute_name, value, description, dataset):
        self.updated_on = updated_on
        self.attribute_name = attribute_name
        self.value = value
        self.description = description
        self.dataset = dataset

    def from_json(self, json):
        self.id = json.get('tag_id', None)
        self.updated_on = json.get('updated_on', None)
        self.attribute_name = json.get('attribute_name', None)
        self.value = json.get('value', None)
        self.description = json.get('description', None)
        self.dataset = json.get('dataset', None)
        return self

    def to_dictionary(self):
        obj = {
            'attribute_id': self.id,
            'updated_on': self.updated_on,
            'attribute_name': self.attribute_name,
            'value': self.value,
            'description': self.description,
        }
        return obj
