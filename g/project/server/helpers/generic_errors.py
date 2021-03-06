from flask import jsonify
from werkzeug import exceptions


def bad_request(message=exceptions.BadRequest().description, exc=None):
    response = {'error': 'Bad Request', 'message': message}
    if exc:
        response['type'] = exc.__class__.__name__
    response = jsonify(response)
    response.status_code = 400
    return response


def forbidden(message=exceptions.Forbidden().description):
    response = jsonify({'error': 'Forbidden', 'message': message})
    response.status_code = 403
    return response


def not_found(message=exceptions.NotFound().description):
    response = jsonify({'error': 'Not Found', 'message': message})
    response.status_code = 404
    return response


def server_error(message):
    response = jsonify({'error': 'Server Error', 'message': message})
    response.status_code = 500
    return response


def unauthorized(error='Unauthorized', message=exceptions.Unauthorized().description):
    response = jsonify({'error': error, 'message': message})
    response.status_code = 401
    return response

def not_implemented(message=exceptions.NotImplemented().description):
    response = jsonify({'error': 'Not Implemented', 'message': message})
    response.status_code = 501
    return response
