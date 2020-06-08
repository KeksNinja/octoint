from octoint.setup.setup_utils import get_profile_dict, write_profile_dict
from octoint.main_utils import octoint_logger

setup_model_logger = octoint_logger(__name__)


def get_profile_names():
    profile_dict = get_profile_dict()
    setup_model_logger.info(f'trying to access profiles {profile_dict}')
    return profile_dict['profiles'].keys()


def create_info_text(key):
    profile_dict = get_profile_dict()
    select_profile = profile_dict['profiles'][key]
    volume = select_profile['volume']
    text = "Model:             {model}\n" \
           "Name:              {name}\n" \
           "Height:            {height}\n" \
           "Width:             {width}\n" \
           "Depth:             {depth}\n" \
           "Heated Bed:        {heatedBed}\n" \
           "Heated Chamber:    {heatedChamber}\n" \
           "Formfactor:        {formFactor}\n" \
        .format(**select_profile, **volume)

    return text


def write_config(setup_widget):
    profile_dict = get_profile_dict()
    key = setup_widget.print_profiles.profiles_menu.currentText()
    config_dict = profile_dict['profiles'][key]
    config_dict['ip_address'] = setup_widget.octopi_settings.ip_address.text()
    config_dict['api_key'] = setup_widget.octopi_settings.api_key.text()
    write_profile_dict(config_dict)


def write_ip_and_api(setup_widget):
    config_dict = {'ip_address': setup_widget.octopi_settings.ip_address.text(),
                   'api_key': setup_widget.octopi_settings.api_key.text()}
    write_profile_dict(config_dict)


def update_info_text(setup_widget):
    key = setup_widget.print_profiles.profiles_menu.currentText()
    new_info_text = create_info_text(key)
    setup_widget.print_profiles.info_label.setText(new_info_text)
