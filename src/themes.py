import json
import os

def list_themes(args):
    print("\nThemes:")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    themes_path = os.path.join(script_dir, '../', 'themes', 'themes.json')
    
    try:
        with open(themes_path, 'r') as file:
            themes = json.load(file)
            sorted_keys = sorted(themes.keys())
            for key in sorted_keys:
                print('- ' + key)
    except FileNotFoundError:
        print(f"File not found: {themes_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {themes_path}")

def set_theme(args):
    return

def active_theme(args):
    return