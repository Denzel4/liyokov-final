from project.server.managers.database import db

class Inspect(db.Base):

    __tablename__ = 'inspect'

    row_id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.String(55), nullable=True)
    human_time = db.Column(db.DateTime, nullable=False)
    cpu = db.Column(db.Float, nullable=False)
    ram = db.Column(db.Float, nullable=False)
    image_size = db.Column(db.String(50), nullable=False)
    spot_name = db.Column(db.String(50), nullable=False)
    thresold = db.Column(db.Float, nullable=False)
    weight_file = db.Column(db.String(120), nullable=False)
    big_label = db.Column(db.Boolean, nullable=False)
    big_status = db.Column(db.String(55), nullable=False)
    base64 = db.Column(db.String(255), nullable=False)
    batch_result = db.Column(db.Boolean, nullable=False)
    camera_ID = db.Column(db.String(55), nullable=False)
    confidence = db.Column(db.String(55), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    label = db.Column(db.String(55), nullable=False)
    orientation = db.Column(db.String(55), nullable=False)