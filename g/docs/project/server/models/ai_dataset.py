from project.server.managers.database import db

class Dataset(db.Model):
    __tablename__ = 'ai_dataset'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    updated_on = db.Column(db.DateTime(), nullable=False, default="2020-01-01 00:00:00")
    dataset = db.Column(db.String(255), nullable=True)
    users = db.Column(db.Integer, nullable=True)
    version = db.Column(db.String(255), nullable=True)
    ai_agent = db.Column(db.String(255), nullable=True)

    def __init__(self, updated_on, dataset, users, ai_agent):
        self.updated_on = updated_on
        self.dataset = dataset
        self.users = users
        self.ai_agent = ai_agent

    def from_json(self, json):
        self.id = json.get('dataset_id', None)
        self.updated_on = json.get('updated_on', None)
        self.dataset = json.get("dataset", None)
        self.users = json.get("users", None)
        self.ai_agent = json.get("ai_agent", None)

        return self

    def to_dictionary(self):
        obj = {
            'dataset_id':self.id,
            'updated_on': self.updated_on,
            'dataset': self.dataset,
            'users': self.users,
            'ai_agent': self.ai_agent,
        }
        return obj