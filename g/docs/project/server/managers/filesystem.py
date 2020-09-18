from project.server import app
import configparser
import os
config = configparser.ConfigParser()

# fs = app.config['ROOT_DIR']


class fs:

    dataset = os.path.dirname(app.instance_path) + '/dataset/'

    def __init__(self, dataset, logs, model):
        self.dataset = config['DEFAULT']['DATASET_DIR']
        self.logs = config['DEFAULT']['DATASET_DIR']
        self.model = config['DEFAULT']['DATASET_DIR']
