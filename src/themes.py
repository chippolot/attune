import json
import os

from config import get_or_create_config, save_config

def get_theme_names():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    themes_path = os.path.join(script_dir, '../', 'themes', 'themes.json')
    try:
        with open(themes_path, 'r') as file:
            themes = json.load(file)
            return themes.keys()
    except FileNotFoundError:
        print(f"File not found: {themes_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {themes_path}")

def list_themes(args):
    print("\nThemes:")
    for key in sorted(get_theme_names()):
        print('- ' + key)

def set_theme(args):
    theme_name = args.theme_name

    themes = get_theme_names()
    if not theme_name in themes:
        print(f"Invalid theme name: {theme_name}")
        list_themes()
        return
    
    config = get_or_create_config()
    if not 'theme' in config:
        config['theme'] = {}
    config['theme']['active'] = args.theme_name
    save_config(config)
    print(f"Set active theme to: {theme_name}")
    return

def active_theme(args):
    config = get_or_create_config()
    if 'theme' in config:
        theme = config['theme']
        if 'active' in theme: 
            print(f"Active Theme: {theme['active']}")
            return
    print("No active theme set")