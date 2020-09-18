from project.server.managers.database import db


class Location(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "auth_locations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.Enum(
         'Canada',
         'United States',
         'Japan',
         name='role_name_type'
     ), unique=True)

    def from_json(self, json):
        self.id = json.get('location_id', None)
        self.location = json.get('location', None)
        return self

    def to_dictionary(self):
        return {
            'location_id': self.id,
            'location': self.location,
        }