from project.server.handlers.database.auth import login_user, logout_user, confirm_user_email, resend_email_confirmation, change_current_password, confirm_user_reset_password


def login():
    return login_user()


def logout():
    return logout_user()


def confirm_email():
    return confirm_user_email()


def resend_confirmation():
    return resend_email_confirmation()


def change_password():
    return change_current_password()


def confirmed_reset_password():
    return confirm_user_reset_password()