from flask import request

from project.server.handlers.database.users import register_user, get_current_user, get_user_list, select_user, \
    update_current_user, reset_password, select_role, patch_current_user, admin_patch_user, \
    admin_delete_user


def register():
    return register_user()


def reset():
    return reset_password()


def get_current():
    return get_current_user()


def get_user():
    return select_user()


def get_list():
    return get_user_list(request.restful)


def update_current():
    return update_current_user()


def patch_current():
    return patch_current_user()


def patch_user(user_id):
    return admin_patch_user(user_id)


def delete_user(user_id):
    return admin_delete_user(user_id)


def get_role():
    return select_role(request.restful)
