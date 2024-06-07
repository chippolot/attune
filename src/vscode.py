import os
import json

def get_settings_path():
    return os.path.join(os.path.expanduser("~"), 'AppData', 'Roaming', 'Code', 'User', 'settings.json')

def set_vscode_theme(theme_name):
    vscode_settings_path = get_settings_path()
    
    # If the settings file doesn't exist, create the necessary directories
    os.makedirs(os.path.dirname(vscode_settings_path), exist_ok=True)
    
    # Load the current settings if the file exists, otherwise start with an empty dictionary
    if os.path.exists(vscode_settings_path):
        with open(vscode_settings_path, 'r') as file:
            settings = json.load(file)
    else:
        settings = {}
    
    # Set the color theme
    settings['workbench.colorTheme'] = theme_name
    
    # Write the updated settings back to the file
    with open(vscode_settings_path, 'w') as file:
        json.dump(settings, file, indent=4)