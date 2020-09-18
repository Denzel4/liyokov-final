import sys

from flask.blueprints import Blueprint
from flask_jwt_extended import jwt_required

from project.server.config import routes
from project.server.decorators import restful
from flask_swagger_ui import get_swaggerui_blueprint


def init_app(app):
    for version in routes.ROUTES:
        SWAGGER_URL = f'/{version}/api/docs'
        API_URL = f'/static/{version}/swagger.json'
        blueprint = Blueprint(version, __name__)
        module = 'project.server.controllers.%s.' % version

        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={
                'app_name': "Sql Module"
            },
        )

        for route in routes.ROUTES[version]:
            endpoint = route.get('endpoint')
            function = route.get('function')
            method = route.get('method')
            rule = route.get('rule')
            opts = route.get('opts', {})
            auth_required = opts.get('auth_required', False)
            __import__(module + endpoint, fromlist=[''])
            view_function = restful.restful(**opts)(getattr(sys.modules[module + endpoint], function))
            if auth_required:
                view_function = jwt_required(restful.restful(**opts)(getattr(sys.modules[module + endpoint], function)))
            blueprint.add_url_rule(
                rule,
                endpoint=endpoint + ' ' + function,
                view_func= view_function,
                methods=[method],
                strict_slashes=False
            )
        app.register_blueprint(blueprint, url_prefix='/' + version)
        app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
