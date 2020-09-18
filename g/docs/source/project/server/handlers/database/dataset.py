import os
from datetime import datetime

from flask import request, send_from_directory

from project.server.controllers.v1 import errors
from project.server.managers.database import db
from project.server.managers.filesystem import fs
from project.server.models import Image
from project.server.models.ai_dataset import Dataset
from project.server.helpers import database, filesystem , generic_errors


def create_dataset():
    # initialize root (parent) of dataset
    filesystem.create_multiple_directories([filesystem.FS.dataset, filesystem.FS.logs, filesystem.FS.model,
                                            filesystem.FS.annotation])
    post_data = request.get_json()
    rows = []
    for row in post_data:
        new_row = Dataset(updated_on=None, dataset=None, ai_agent=None, users=None)
        new_row.from_json(row)
        rows.append(new_row)
    db.session.add_all(rows)
    print(rows)
    db.session.commit()
    for row in rows:
        filesystem.create_directory(os.path.join(filesystem.FS.dataset, str(row.id)))



def get_dataset(dataset_id):
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        return dataset.to_dictionary()
    except Exception as e:
        print(e)
        return errors.not_found(message='not_found')


def get_dataset_list(restful):
    query = Dataset.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Dataset.area])
    query = query.order_by(*database.get_order_by(Dataset, restful.order_by))
    return database.get_list(query, restful.pagination)


def get_list(restful):
    query = Dataset.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Dataset.area])
    query = query.order_by(*database.get_order_by(Dataset, restful.order_by))
    return database.get_list(query, restful.pagination)


def update_dataset(dataset_id):
    data = request.get_json()
    new_dataset = data.get('dataset', None)
    if new_dataset is not None:
        sets = db.session.query(Dataset).filter_by(dataset=new_dataset).all()
        if len(sets) > 0:
            return generic_errors.not_implemented(f"This dataset name '{new_dataset}' already exists in the database.")
    db.session.query(Dataset).filter_by(id=dataset_id).update(data)
    db.session.commit()


def delete_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    db.session.delete(dataset)
    db.session.commit()


def add_images_in_dataset(dataset_id):
    files = request.files.getlist("files")
    count = 0
    for file in files:
        path = f'{fs.dataset}{dataset_id}/{file.filename}'
        try:
            file.save(path)
            image = Image(
                image_path=path,
                filename=file.filename,
                dataset_id=dataset_id,
                updated_on=datetime.now()
            )
            db.session.add(image)
            db.session.commit()

            count = count + 1
        except FileNotFoundError as e:
            print(e.strerror)
            return errors.server_error(e.strerror)


    return {
        'image_count': count
    }



def get_dataset_images(dataset_id):
    images = db.session.query(Image).filter_by(dataset_id=dataset_id).all()
    return images


def get_dataset_image(dataset, filename):
    return send_from_directory(f'{fs.dataset}/{dataset}', filename, as_attachment=True)


def delete_dataset_image(image_id):
    image = Image.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
