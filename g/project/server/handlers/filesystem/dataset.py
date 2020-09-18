from flask import request, send_from_directory

from project.server.managers.filesystem import fs
import os


def insert_dataset():
    data = request.get_json()
    try:
        os.makedirs(fs.dataset + data.get('dataset'))
        print(fs.dataset + data.get('dataset'))
    except FileExistsError:
        # directory already exists
        print(fs.dataset + data.get('dataset'))
        pass

def delete_dataset(dataset_name):
    try:
        os.rmdir(fs.dataset + dataset_name)
    except FileExistsError:
        # directory already exists
        pass

def rename_dataset(dataset_name):
    post_data = request.get_json()
    new_dataset = post_data.get('dataset')
    os.rename(fs.dataset + dataset_name, fs.dataset + new_dataset)


def select_dataset(restful):
    list = next(os.walk(fs.dataset))[1]
    return {
        "result":list
    }


def get_image_from_path(dataset, filename):
    return send_from_directory(f'{fs.dataset}/{dataset}', filename, as_attachment=True)
