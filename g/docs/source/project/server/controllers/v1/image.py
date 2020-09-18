from flask import request
# from project.server.handlers.database.image import insert_images
from project.server.helpers.bucket import download_file
from project.server.handlers.database.image_attribute import select_all_attributes, update_all_attributes ,\
                                                select_by_dataset, delete_by_dataset, update_by_dataset
from project.server.handlers.filesystem.dataset import insert_dataset, select_dataset, delete_dataset, rename_dataset, \
    get_image_from_path



def download_image(image_id):
    return download_file(image_id)

def upload_image():
    return "upload_images()"

def get_image_list():
    return "select_image_list(request.restful)"

def get_all_attributes():
    return select_all_attributes(request.restful)

def change_all_attributes():
    return update_all_attributes()

def change_image():
    return "insert_image()"

def get_attributes_by_dataset():
    return select_by_dataset()

def delete_attributes_by_dataset():
    return delete_by_dataset()

def update_attributes_by_dataset():
    return update_by_dataset()
