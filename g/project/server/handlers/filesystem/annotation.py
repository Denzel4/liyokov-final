from flask import request
from project.server.managers.filesystem import fs
import os


def insert_annotation():
    data = request.get_json()
    try:
        os.makedirs(fs + data.get('annotation_path'))
        print(fs + data.get('annotation_path'))
    except FileExistsError:
        # directory already exists
        print(fs + data.get('dataset'))
        pass


def rename_dataset(dataset_name, new_dataset):
    os.rename(dataset_name, fs + new_dataset)


def select_dataset(restful):
    list = next(os.walk(fs))[1]
    return {
        "result":list
    }