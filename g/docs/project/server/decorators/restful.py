import pyparsing
import re

from flask import jsonify, request, Response
from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from jwt import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Response as WerkzeugResponse

from project.server.factories import error
from project.server.helpers import marshaller
from project.server.managers import logger
from project.server.objects.restful import Restful


def _is_roles_valid(auth_roles):
    claims = get_jwt_claims()
    for role in auth_roles:
        if role in claims['roles']:
            return True

    return False


def __get_fields(data, fields):
    left_par = pyparsing.Literal('(')
    right_par = pyparsing.Literal(')')
    field = pyparsing.Combine(pyparsing.Word(pyparsing.alphanums + '_') + pyparsing.Optional('*')) | '*'
    nested_field = pyparsing.Forward()
    nested_field << pyparsing.Combine(
        field +
        left_par +
        pyparsing.Or(nested_field | field) +
        pyparsing.ZeroOrMore(pyparsing.Word(',') + pyparsing.Or(nested_field | field)) +
        right_par
    )
    root_fields = pyparsing.Or(nested_field | field) +\
        pyparsing.ZeroOrMore(pyparsing.Suppress(',') + pyparsing.Or(nested_field | field))

    for parser in root_fields.parseString(fields).asList():
        match = re.compile('([\w ]+|\*)([\w,*() ]+\))?(\*?)').match(parser)
        name = match.group(1)
        include_all = match.group(2) == '(*)'
        recursive = match.group(3) == '*'

        if recursive:
            data[name] = True
        elif include_all:
            data[name] = '*'
        elif match.group(2) is not None:
            data[name] = {}
            sub_fields = re.search('^\((.*)\)$', match.group(2)).group(1)
            __get_fields(data[name], sub_fields)
        else:
            data[name] = {}

    return data


def __get_json_clean_response(return_value):
    if isinstance(return_value, dict):
        return_value = {'data': return_value}
    elif return_value is None:
        return_value = {}
    elif isinstance(return_value, list):
        items = []
        for item in return_value:
            if not isinstance(item, dict):
                items.append(item.to_dictionary())
            else:
                items.append(item)
            return_value = items
    elif isinstance(return_value, object):
        try:
            return_value = {'data': return_value.to_dictionary()}
        except AttributeError:
            pass
    return jsonify(return_value)


def __get_json_response(return_value, use_pagination):
    if isinstance(return_value, dict):
        return_value = {'data': return_value}
    elif return_value is None:
        return_value = {}
    elif isinstance(return_value, list):
        items = []
        for item in return_value:
            if not isinstance(item, dict):
                items.append(item.to_dictionary())
            else:
                items.append(item)
            return_value = items
    elif isinstance(return_value, object):
        try:
            return_value = {'data': return_value.to_dictionary()}
        except AttributeError:
            pass

    return_value = marshaller.marshal(return_value, request.restful.fields)

    if use_pagination:
        return_value = {
            'items': return_value,
            'pagination': {
                'count': len(return_value),
                'limit': request.restful.pagination.limit,
                'offset': request.restful.pagination.offset,
                'total_count': request.restful.pagination.total_count
            }
        }
    return jsonify(return_value)


def __get_restful_object(max_pagination_limit):
    obj = Restful()

    args = dict((k, v) for k, v in request.args.items())

    fields = args.get('fields', None)
    if fields is not None:
        obj.fields = __get_fields({}, fields)
        del args['fields']

    limit = args.get('limit', None)
    if limit is not None:
        limit = int(limit)
        if max_pagination_limit != 0 and (limit == 0 or limit > max_pagination_limit):
            limit = max_pagination_limit
        obj.pagination.limit = limit
        del args['limit']

    offset = args.get('offset', None)
    if offset is not None:
        obj.pagination.offset = int(offset)
        del args['offset']

    order_by = args.get('order_by', None)
    if order_by is not None:
        for values in str(order_by).split(','):
            key_value = values.split(':')
            obj.order_by[key_value[0].lower()] = key_value[1].lower()
        del args['order_by']

    q = args.get('q', None)
    if q is not None:
        obj.q = q
        del args['q']

    obj.filters = args

    return obj


def restful(**opts):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_required = opts.get('auth_required', False)
            auth_roles = opts.get('auth_roles', None)
            max_pagination_limit = opts.get('max_pagination_limit', 50)
            use_pagination = opts.get('use_pagination', False)
            request.route_options = opts
            request.function = f
            try:
                if auth_required:
                    try:
                        verify_jwt_in_request()
                    except Exception:
                        return error.get_instance(request.path).unauthorized(error='Unauthenticated')
                    else:
                        if auth_roles is None:
                            pass
                        else:
                            if not _is_roles_valid(auth_roles):
                                return error.get_instance(request.path).unauthorized()
                setattr(request, 'restful', __get_restful_object(max_pagination_limit))
                return_value = f(*args, **kwargs)
                if isinstance(return_value, Response) or isinstance(return_value, WerkzeugResponse):
                    return return_value
                return __get_json_response(return_value, use_pagination)
            except ExpiredSignatureError as exc:
                return error.get_instance(request.path).unauthorized(exc.args)
            except (NotFound, NoResultFound):
                return error.get_instance(request.path).not_found()
            except IntegrityError as exc:
                return error.get_instance(request.path).bad_request(exc.orig.diag.message_detail, exc)
            except Exception as exc:
                logger.exception(exc.args)
                return error.get_instance(request.path).server_error(exc.args)

        return wrapped
    return decorator
