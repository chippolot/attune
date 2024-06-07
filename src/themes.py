import json
import os

from config import get_or_create_config, save_config, get_repo_file_path
from windows import set_wallpaper, set_windows_mode
from dotfiles import replace_dotfile_line, DotfileSource

def get_themes_config():
    themes_path = get_repo_file_path('themes/themes.json')
    try:
        with open(themes_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {themes_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {themes_path}")

def get_theme_config(theme_name):
    themes = get_themes_config()
    if not theme_name in themes:
        return None
    return themes[theme_name]

def get_theme_names():
    themes = get_themes_config()
    return themes.keys()

def list_themes(args):
    print("\nThemes:")
    for key in sorted(get_theme_names()):
        print('- ' + key)

def set_theme(args):
    theme_name = args.theme_name

    # Validate theme name and get config
    theme = get_theme_config(theme_name)
    if theme == None:
        print(f"Invalid theme name: {theme_name}")
        list_themes()
        return
    
    # Set Background
    if 'background' in theme:
        background_file = theme['background']
        print(f"Seting background to: '{background_file}'")
        background_path = get_repo_file_path(f'themes/backgrounds/{background_file}', validate=True)
        set_wallpaper(background_path)

    # Set Display Mode
    if 'display_mode' in theme:
        display_mode = theme['display_mode']
        if display_mode in ['light', 'dark']:
            print(f"Seting display mode to: '{display_mode}'")
            set_windows_mode(display_mode == 'dark')
        else:
            print(f"Invalid display mode: {display_mode}")

    # Set Oh My Posh Theme
    if 'prompt' in theme:
        prompt_file = theme['prompt']
        print(f"Seting prompt theme to: '{prompt_file}'")
        prompt_path = os.path.abspath(get_repo_file_path(f'themes/prompts/{prompt_file}', validate=True))
        replace_dotfile_line(DotfileSource.ATTUNE, '.env', r'export OMP_THEME=.*', f'export OMP_THEME="{prompt_path}"')

    
    # Set active theme name and save config
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