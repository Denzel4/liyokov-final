import datetime
from project.server.helpers.serialize import get_json_clean_response
from project.server.helpers.encrypter import encrypt_password
from project.server.managers.database import db
from project.server.models.auth_role import Role
from project.server.models.auth_location import Location

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('auth_users.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('auth_roles.id', ondelete='CASCADE')),
)


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "auth_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255, collation='utf8_unicode_ci'), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255, collation='utf8_unicode_ci'), nullable=False)
    last_name = db.Column(db.String(255, collation='utf8_unicode_ci'), nullable=False)
    registered_on = db.Column(db.DateTime(), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    company = db.Column(db.String(255))
    title = db.Column(db.String(255))
    language = db.Column(db.String(255), nullable=False)
    admin_validation = db.Column(db.Boolean, nullable=False, default=False)
    location_id = db.Column(db.Integer, db.ForeignKey('auth_locations.id', ondelete='CASCADE'), nullable=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'),
                            post_update=True)
    location = db.relationship(Location, primaryjoin=location_id == Location.id, post_update=True, uselist=False)

    def __init__(self, username, password, email, first_name, last_name, language='en', company=None,
                 title=None, confirmed=False, confirmed_on=None, admin_validation=False, roles='PENDING', location_id=1):
        self.username = username
        self.password = encrypt_password(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.title = title
        self.language = language
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.admin_validation = admin_validation
        self.location_id = location_id
        self.location = Location.query.filter_by(id=location_id).one()
        # role = Role.query.filter_by(name='ADMIN').one()
        self.roles = roles.query(roles).last()

        new_roles = []

        if roles is not None:
            if roles == 'ADMIN':
                role = Role.query.filter_by(name='ADMIN').one()
                new_roles.append(role)
            elif roles == 'ANNOTATOR':
                role = Role.query.filter_by(name='ANNOTATOR').one()
                new_roles.append(role)
            else:
                role = Role.query.filter_by(name='VIEWER').one()
                new_roles.append(role)
            self.roles = new_roles
        else:
            role = Role.query.filter_by(name='VIEWER').one()
            new_roles.append(role)
            self.roles = new_roles

    def from_partial_json(self, dictionary):
        super(User, self).from_partial_json(dictionary)
        if 'password' in dictionary:
            self.password = encrypt_password(dictionary.get('password'))
        self.registered_on = datetime.datetime.now()
        return self

    def from_json(self, json):
        self.id = json.get('user_id', None)
        self.email = json.get('email', None)
        self.password = json.get('password', None)
        self.first_name = json.get('first_name', None)
        self.last_name = json.get('last_name', None)
        self.roles = json.get('roles', None)
        return self

    def to_dictionary(self):
        obj = {
            'admin_validation': self.admin_validation,
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_login_at': self.last_login_at,
            'registered_on': self.registered_on,
            'confirmed': self.confirmed,
            'confirmed_on': self.confirmed_on,
            'company': self.company,
            'title': self.title,
            'language': self.language,
            'roles': [role.name for role in self.roles],
            'location': [get_json_clean_response(self.location)]
        }
        return obj
