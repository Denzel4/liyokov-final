from datetime import datetime

import itsdangerous
from flask import request
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from itsdangerous import URLSafeTimedSerializer

from project.server.helpers.encrypter import encrypt_password
from project.server import app
from project.server.controllers.v1 import errors
from project.server.helpers.auth import get_auth_token, send_confirmation_email
from project.server.managers.bcrypt import bcrypt
from project.server.managers.database import db
from project.server.models.auth_blacklist_token import BlacklistToken
from project.server.models.auth_user import User
from project.server.helpers.auth import send_new_user_email


def __confirm_token(token, expiration=None):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except itsdangerous.exc.SignatureExpired:
        return False
    return email


def confirm_user_email():
    post_data = request.get_json()

    try:
        email = __confirm_token(post_data['token'], expiration=3600)
    except Exception as e:
        return errors.forbidden('invalid_confirmation_token')

    if isinstance(email, str):
        user = User.query.filter_by(
            email=email
        ).first()

        user.confirmed = True
        user.confirmed_on = datetime.now()

        db.session.add(user)
        db.session.commit()
        send_new_user_email(user, ["macula@creationauts.com", "sabrina@creationauts.com", "meeta@creationauts.com"])
    else:
        return errors.forbidden('expired_confirmation_token')


def confirm_user_reset_password():
    post_data = request.get_json()

    try:
        email = __confirm_token(post_data['token'], expiration=3600)
    except Exception as e:
        return errors.forbidden('invalid_confirmation_token')

    if isinstance(email, str):
        user = User.query.filter_by(
            email=email
        ).first()
        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.password = encrypt_password(post_data['password'])

        db.session.commit()
    else:
        return errors.forbidden('expired_confirmation_token')


def resend_email_confirmation():
    post_data = request.get_json()

    try:
        email = __confirm_token(post_data['token'])
        send_confirmation_email(app, email)
    except Exception as e:
        return errors.forbidden('invalid_confirmation_token')


def login_user():
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter(
                or_(
                    User.username == post_data.get('username'),
                    User.email == post_data.get('username')
                )
        ).first()

        if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
        ):
            if user.admin_validation != 1:
                return errors.forbidden('access_not_granted')

            if user.confirmed:
                auth_token = create_access_token(identity=user)
                user.last_login_at = datetime.now()

                db.session.add(user)
                db.session.commit()

                user = user.to_dictionary()
                if auth_token:
                    return {
                        'auth_token': auth_token,
                        'roles': user['roles']
                    }
            else:
                return errors.forbidden('email_not_confirmed')
        else:
            return errors.not_found('invalid_user')
    except Exception as e:
        print(e)
        return errors.server_error('unknown_error')


def logout_user():
    auth_token = get_auth_token(request)

    if auth_token:
        verify_jwt_in_request()

        # check if user already exists
        existing_blacklisted_token = BlacklistToken.query.filter_by(token=auth_token).first()

        if existing_blacklisted_token:
            return

        try:
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)

            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()

        except Exception as e:
            return errors.server_error(e)
    else:
        return errors.forbidden('provide_valid_token')


def change_current_password():
    # username = get_jwt_identity()
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    current_password = data.get('current_password')
    new_password, new_confirm_password = data.get('new_password'), data.get('new_password')
    if bcrypt.check_password_hash(user.password, current_password):
        if new_password == new_confirm_password:
            user.password = encrypt_password(new_password)
            db.session.commit()
            return {
               "user": user.to_dictionary()
            }
        else:
            return errors.server_error(message="password_not_matching")

    return errors.forbidden(message='wrong_password')