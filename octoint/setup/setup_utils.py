import yaml

from octoint.main_config import config_path
from octoint.main_utils import octoint_logger

setup_utils_logger = octoint_logger(__name__)


def get_profile_dict():
    from octoint import client
    try:
        return client._get('/api/printerprofiles')
    except AttributeError as e:
        setup_utils_logger.error(e)
        return {}


def build_config_dict_from_profile(profile_dict: dict):
    connectors = ['api_key', 'ip_address']
    config_dict = {'connection': {key: profile_dict.get(key, 'None') for key in connectors}}

    try:
        printprofile = {}
        descriptors = ['id', 'model', 'name', 'resource']
        printprofile.update({key: profile_dict.get(key, 'None') for key in descriptors})

        coordinates = ['width', 'depth', 'height']
        rename = ['x', 'y', 'z']
        printprofile.update({rename[index]: profile_dict['volume'][key] for index, key in enumerate(coordinates)})
        config_dict.update({'printprofile': printprofile})
    except KeyError:
        pass

    return config_dict


def write_profile_dict(profile_dict):
    setup_utils_logger.info(f'writing {profile_dict} to {config_path}')
    config_dict = build_config_dict_from_profile(profile_dict)
    with open(config_path, 'w') as config_file:
        yaml.dump(config_dict, config_file)
