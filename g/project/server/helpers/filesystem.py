from project.server import app
import configparser
import os
config = configparser.ConfigParser()


def create_directory(path):
    # if the path is not existed yet
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False


def create_multiple_directories(paths):
    all_existed = True
    for path in paths:
        if create_directory(path):
            all_existed = False
    return all_existed


class FS:
    config = configparser.ConfigParser()
    config.read("project/server/config/paths.conf")
    dataset = os.path.join(os.path.dirname(app.instance_path), config['DEFAULT']['DATASET_DIR'])
    logs = os.path.join(os.path.dirname(app.instance_path), config['DEFAULT']['LOG_DIR'])
    model = os.path.join(os.path.dirname(app.instance_path), config['DEFAULT']['MODEL_DIR'])
    annotation = os.path.join(os.path.dirname(app.instance_path), config['DEFAULT']['ANNOTATION_DIR'])
