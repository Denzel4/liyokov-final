from flask import request
from project.server.handlers.database.camera import insert_preset, select_all_camera

def save_preset():
    return insert_preset()

def select_all_preset():
    return select_all_camera(request.restful)