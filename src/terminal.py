import os
import json

from dict import set_dict_value

def get_settings_path():
    return os.path.join(
        os.path.expanduser("~"),
        'AppData',
        'Local',
        'Packages',
        'Microsoft.WindowsTerminal_8wekyb3d8bbwe',
        'LocalState',
        'settings.json')


def get_settings():
    settings_path = get_settings_path()
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            settings = json.load(file)
    else:
        settings = {}
    return settings

def save_settings(settings): 
    with open(get_settings_path(), 'w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4)

def set_terminal_profile_param(path, value):
    if value == None:
        return

    settings_path = get_settings_path()
    if not os.path.exists(settings_path):
        print(f"Configuration file not found: {settings_path}")
        return

    # Update font settings in all profiles
    settings = get_settings()
    profiles = settings.get("profiles", {})
    defaults = profiles.get("defaults", {})
    set_dict_value(defaults, path, value)
    for profile in profiles.get("list", []):
        set_dict_value(profile, path, value)
    save_settings(settings)

def set_terminal_color_scheme(name, color_scheme_path):
    if not os.path.exists(color_scheme_path):
        raise FileNotFoundError(f"The file {color_scheme_path} does not exist.")
    
    with open(color_scheme_path, 'r') as file:
        color_scheme = json.load(file)
    
    settings = get_settings()

    # Update existing scheme
    schemes = settings.get("schemes", [])
    scheme_found = False
    for other_scheme in schemes:
        if 'name' in other_scheme and other_scheme['name'] == name:
            other_scheme.clear()
            other_scheme.update(color_scheme)
            scheme_found = True
            break
    
    # Add new scheme if none was found
    if not scheme_found:
        schemes.append(color_scheme)

    save_settings(settings)
