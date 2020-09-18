from datetime import datetime

from flask import request
from flask_jwt_extended import get_jwt_identity, create_access_token
from sqlalchemy import or_, and_

from project.server import app
from project.server.controllers.v1 import errors
from project.server.helpers.auth import send_confirmation_email, get_auth_token
from project.server.helpers import database
from project.server.managers.database import db
from project.server.models import BlacklistToken
from project.server.models.auth_user import User, roles_users
from project.server.models.auth_role import Role
from project.server.helpers.serialize import get_json_clean_response
from project.server.helpers.auth import send_activation_account, send_reset_email

def register_user():
    # get the post data
    post_data = request.get_json()

    # check if user already exists
    user = User.query.filter(
        or_(
            User.username == post_data.get('username'),
            User.email == post_data.get('email')
        )
    ).first()

    if not user:
        try:
            user = User(
                username=post_data.get('username'),
                password=post_data.get('password'),
                email=post_data.get('email'),
                first_name=post_data.get('first_name'),
                last_name=post_data.get('last_name'),
                company=post_data.get('company'),
                roles=post_data.get('roles'),
            )

            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                send_confirmation_email(app, user.email)
            else:
                user.confirmed = True
                user.confirmed_on = datetime.now()

            # insert the user
            db.session.add(user)
            db.session.commit()

            return {
                'user': user.to_dictionary(),
            }
        except Exception as e:
            errors.unauthorized(e)
    else:
        message = 'user_already_exists'
        if user.username == post_data.get('username'):
            message = 'username_already_used'
        elif user.email == post_data.get('email'):
            message = 'email_already_used'

        return errors.bad_request(message=message)


def reset_password():
    # get the post data
    post_data = request.get_json()

    # check if user already exists
    user = User.query.filter(User.email == post_data.get('email')).first()

    if user:
        try:
            '''
            user = User(
                password=post_data.get('password'),
            )

            '''
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                send_reset_email(app, post_data.get('email'))
            else:
                user.confirmed = True
                user.confirmed_on = datetime.now()

            # insert the user
            db.session.add(user)
            db.session.commit()

            return {
                'user': user.to_dictionary(),
            }
        except Exception as e:
            errors.unauthorized(e)
    else:
        message = 'user_already_exists'
        if user.username == post_data.get('username'):
            message = 'username_already_used'
        elif user.email == post_data.get('email'):
            message = 'email_already_used'

        return errors.bad_request(message=message)


def get_current_user():
    username = get_jwt_identity()
    if isinstance(username, str):
        user = User.query.filter_by(username=username).first()
        return user.to_dictionary()

    return errors.unauthorized(message='login_required')


def select_user():
    post_data = request.get_json()
    username = post_data.get('username')
    print(username)
    if isinstance(username, str):
        user = User.query.filter_by(username=username).first()
        return user.to_dictionary()

    return errors.unauthorized(message='login_required')

def get_user_list(restful):
    query = User.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [User.username, User.first_name, User.last_name, User.email])
    query = query.order_by(*database.get_order_by(User, restful.order_by))
    return database.get_list(query, restful.pagination)


def select_role(restful):
    query = Role.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [User.username, User.first_name, User.last_name, User.email])
    query = query.order_by(*database.get_order_by(User, restful.order_by))
    return database.get_list(query, restful.pagination)

def update_current_user():
    # username = get_jwt_identity()
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    print(user.roles)
    user.company = data.get('company')
    user.confirmed = data.get('confirmed')
    user.confirmed_on = datetime.now()
    user.email = data.get('email')
    user.first_name = data.get('first_name')
    user.language = data.get('language')
    user.last_name = data.get('last_name')
    user.registered_on = datetime.now()
    if data.get('admin_validation') == 1:
        user.admin_validation = 1
        send_activation_account(user, user.email)
    else:
        user.admin_validation = data.get('admin_validation')
    if len(user.roles) == 0:
        role = Role.query.filter_by(name=data.get('roles')[0]).one()
        user.roles.append(role)
    else:
        role = Role.query.filter_by(name=data.get('roles')[0]).one()
        user.roles.remove(user.roles[0])
        user.roles.append(role)
    user.username = data.get('username')
    db.session.commit()
    return {
                'user': user.to_dictionary(),
            }


def patch_current_user():
    username = get_jwt_identity()
    data = request.get_json()
    auth_token = None
    user = User.query.filter_by(username=username).first()
    if data.get('company'):
        user.company = data.get('company')
    if data.get('email'):
        # check if email already used
        existing_user = User.query.filter(
            and_(
                User.id != user.id,
                User.email == data.get('email')
            )
        ).first()
        if not existing_user:
            user.email = data.get('email')
        else:
            return errors.bad_request(message='email_already_used')
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')

    try:
        if data.get('role'):
            user.roles = data.get('role')
    except:
        pass
    db.session.add(user)
    db.session.commit()

    return {
        'auth_token': auth_token if auth_token else None,
        'user': user.to_dictionary(),
    }


def admin_patch_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    if data.get('company') is not None:
        user.company = data.get('company')
    if data.get('email') is not None:
        # check if email already used
        existing_user = User.query.filter(
            and_(
                User.id != user_id,
                User.email == data.get('email')
            )
        ).first()
        if not existing_user:
            user.email = data.get('email')
        else:
            return errors.bad_request(message='email_already_used')
    if data.get('first_name') is not None:
        user.first_name = data.get('first_name')
    if data.get('last_name') is not None:
        user.last_name = data.get('last_name')
    if data.get('admin_validation') is not None:
        user.admin_validation = data.get('admin_validation')

    if data.get('roles') is not None:
        roles = []
        if data.get('roles') == 'ADMIN':
            role = Role.query.filter_by(name='ADMIN').one()
            roles.append(role)
        elif data.get('roles') == 'ANNOTATOR':
            role = Role.query.filter_by(name='VIEWER').one()
            roles.append(role)
        else:
            role = Role.query.filter_by(name='VIEWER').one()
            roles.append(role)
        user.roles = roles

    db.session.add(user)
    db.session.commit()

    return {
        'user': user.to_dictionary(),
    }


def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return {
        'user': user.to_dictionary()
    }
