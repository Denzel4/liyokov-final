from project.server.managers.database import db

class Agent(db.Model):
    __tablename__ = 'ai_agent'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    updated_on = db.Column(db.DateTime(), nullable=False, default="2020-01-01 00:00:00")
    camera_id = db.Column(db.Integer, nullable=True)
    model_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    environment = db.Column(db.String(255), nullable=True)
    project = db.Column(db.String(255), nullable=True)
    session = db.Column(db.String(255), nullable=True)
    user = db.Column(db.String(255), nullable=True)
    random_flip = db.Column(db.String(255), nullable=True, default='NULL')
    brightness = db.Column(db.String(255), nullable=True, default='NULL')
    random_rotate = db.Column(db.String(255), nullable=True, default='NULL')
    random_crop = db.Column(db.String(255), nullable=True, default='NULL')

    def __init__(self, camera_id, model_id, description, environment, project, session, user, random_flip, brightness, random_rotate, random_crop):
        self.camera_id = camera_id
        self.model_id = model_id
        self.description = description
        self.environment = environment
        self.project = project
        self.session = session
        self.user = user
        self.random_flip = random_flip
        self.brightness = brightness
        self.random_rotate = random_rotate
        self.random_crop = random_crop

    def from_json(self, json):
        self.id = json.get('agent_id', None)
        self.camera_id = json.get('camera_id', None)
        self.model_id = json.get("model_id", None)
        self.description = json.get("description", None)
        self.environment = json.get("environment", None)
        self.project = json.get("project", None)
        self.session = json.get("session", None)
        self.user = json.get("user", None)
        self.random_flip = json.get("random_flip", None)
        self.brightness = json.get("brightness", None)
        self.random_rotate = json.get("random_rotate", None)
        self.random_crop = json.get("random_crop", None)

        return self

    def to_dictionary(self):
        obj = {
            'agent_id':self.id,
            'camera_id': self.camera_id,
            'model_id': self.model_id,
            'description': self.description,
            'environment': self.environment,
            'project': self.project,
            'session': self.session,
            'user': self.user,
            'random_flip': self.random_flip,
            'brightness': self.brightness,
            'random_rotate': self.random_rotate,
            'random_crop': self.random_crop
        }
        return obj
