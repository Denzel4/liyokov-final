from project.server.managers.database import db


class Category(db.Model):
    """ Models Model for storing model related details """
    __tablename__ = "ai_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_on = db.Column(db.DateTime(), nullable=False)
    category_name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    dataset = db.Column(db.Integer,  nullable=False)

    def __init__(self, updated_on, category_name, value, description, dataset):
        self.updated_on = updated_on
        self.category_name = category_name
        self.value = value
        self.description = description
        self.dataset = dataset

    def from_json(self, json):
        self.id = json.get('tag_id', None)
        self.updated_on = json.get('updated_on', None)
        self.category_name = json.get('category_name', None)
        self.value = json.get('value', None)
        self.description = json.get('description', None)
        self.dataset = json.get('dataset', None)
        return self

    def to_dictionary(self):
        obj = {
            'category_id': self.id,
            'updated_on': self.updated_on,
            'category_name': self.category_name,
            'value': self.value,
            'description': self.description,
            'dataset': self.dataset
        }
        return obj