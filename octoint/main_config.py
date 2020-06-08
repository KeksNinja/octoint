import os
import yaml

from octoint.main_utils import octoint_logger

main_config_logger = octoint_logger(__name__)

config_path = './config.yaml'
config_dict = {}


def load_config():
    global config_dict
    if os.path.exists(config_path):
        with open('./config.yaml') as yaml_file:
            config_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)


class Config:
    def __init__(self):
        pass

    @property
    def dimensions(self):
        """
        Load Dimensions from Config file
        :return:(dict) x, y, z dimensions of the printer
        """

        return {'x': config_dict['printprofile']['x'],
                'y': config_dict['printprofile']['y'],
                'z': config_dict['printprofile']['z']
                }

    @property
    def address(self):
        return f"http://{config_dict['connection']['ip_address']}/"

    @property
    def ip(self):
        return config_dict['connection']['ip_address']

    @property
    def api_key(self):
        return config_dict['connection']['api_key']

    @property
    def print_model(self):
        return config_dict['printprofile']['model']

    @classmethod
    def reload_config(cls):
        load_config()


CONFIG = Config()
