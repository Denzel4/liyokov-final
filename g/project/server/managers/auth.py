from flask import jsonify
from flask_jwt_extended import (
    JWTManager
)

from project.server.controllers.v1 import errors
from project.server.helpers.auth import check_blacklist

jwt = JWTManager()


def init_app(app):
    global jwt
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'roles': [role.name for role in user.roles]}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.username

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decrypted_token):
        return check_blacklist(decrypted_token)

    @jwt.expired_token_loader
    def expired_token_callback(token):
        return errors.unauthorized(error='token_expired', message='The token has expired')

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return errors.unauthorized(error='invalid_token', message='Signature verification failed')

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return errors.unauthorized(error='authorization_required', message='Request does not contain an access token')

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return errors.unauthorized(error='fresh_token_required', message='The token is not fresh')

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return errors.unauthorized(error='token_revoked', message='The token has been revoked')