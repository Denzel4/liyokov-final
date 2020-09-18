from project.server.config import routes
import json
from zLastGame import GetRouteProcessor as grp
from zLastGame import DeleteRouteProcessor as drp
from zLastGame import PutRouteProcessor as prp
from zLastGame import AuthRouteProcessor as authrp
from zLastGame import PostRouteProcessor as postrp
import zLastGame.ModelDefinition as md


def get_meta_data():
    meta_data = {
        "openapi": "3.0.0",
        "info": {
            "description": "Sql Module Development",
            "version": "1.0.0",
            "title": "Sql Module Development",
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "/v1"
            }
        ]
    }
    return meta_data


def get_merge_paths(p1, p2):
    paths = p1.copy()
    # merge paths
    for route_name in p1.keys():
        if route_name in p2.keys():
            for method_name, value in p2[route_name].items():
                paths[route_name][method_name] = value

    for route_name in p2.keys():
        if route_name not in p1.keys():
            paths[route_name] = p2[route_name]
    return paths


def main():
    # md.main()
    get_meta_data()
    data = get_meta_data()
    # get_paths = grp.get_paths(routes)
    # delete_paths = drp.get_paths(routes)
    # post_paths =
    postrp.get_paths(routes)
    data['paths'] = get_merge_paths(
        get_merge_paths(grp.get_paths(routes),
                        drp.get_paths(routes)),
        get_merge_paths(prp.get_paths(routes),
                        authrp.get_paths(routes))
    )
    #
    # # data['paths'] = postrp.get_paths(routes)
    data['components'] = {'schemas': md.get_model_info(),
                          'securitySchemes': {
                              'BearerAuth': {
                                  "type": "http",
                                  "scheme": "bearer",
                                  "bearerFormat": "JWT"
                              }
                          }
                          }
    json.dump(data, open("project/server/static/v1/swagger.json", "w"))


if __name__ == "__main__":
    main()
