from project.server.handlers.database.dataset import create_dataset, update_dataset, get_dataset, get_dataset_list, \
    delete_dataset, add_images_in_dataset, get_dataset_images, get_dataset_image, delete_dataset_image


def create():
    return create_dataset()


def get(dataset_id):
    return get_dataset(dataset_id)


def get_list(restful):
    return get_dataset_list(restful)


def update(dataset_id):
    return update_dataset(dataset_id)


def delete(dataset_id):
    return delete_dataset(dataset_id)


def add_images(dataset_id):
    return add_images_in_dataset(dataset_id)


def get_images(dataset_id):
    return get_dataset_images(dataset_id)


def get_image(dataset_id, filename):
    return get_dataset_image(dataset_id, filename)


def delete_image(image_id):
    return delete_dataset_image(image_id)