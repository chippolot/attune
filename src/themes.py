import json
import os
import argparse

from config import get_or_create_config, save_config, get_repo_file_path
from windows import set_wallpaper, set_windows_mode
from dotfiles import replace_dotfile_line, DotfileSource
from vscode import set_vscode_theme, set_vscode_font
from fonts import get_font_config

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
    if isinstance(args, argparse.Namespace):
        theme_name = args.theme_name
    else:
        theme_name = args

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


    # Set VSCode Theme
    if 'code' in theme:
        code_theme = theme['code']
        print(f"Seting code to: '{code_theme['name']}'")
        set_vscode_theme(code_theme['name'], code_theme.get('extension'))
        
        if 'font' in code_theme:
            font = code_theme['font']
            font_id = font.get("id")
            font_config = get_font_config(font_id, validate=True)
            if font_config != None:
                font_family = font_config.get("family") 
                font_size = font.get("size")
                set_vscode_font(font_family, font_size)

    # Set active theme name and save config
    config = get_or_create_config()
    if not 'theme' in config:
        config['theme'] = {}
    config['theme']['active'] = theme_name
    save_config(config)
    print(f"Set active theme to: {theme_name}")
    return

def get_active_theme_name():
    config = get_or_create_config()
    if 'theme' in config:
        theme = config['theme']
        if 'active' in theme: 
            return theme['active']
    return None

def get_default_theme_name():
    config = get_or_create_config()
    if 'theme' in config:
        theme = config['theme']
        if 'default' in theme: 
            return theme['default']
    return None

def active_theme(args):
    active_theme_name = get_active_theme_name()
    if active_theme_name != None:
        print(f"Active Theme: {active_theme_name}")
    else:
        print("No active theme set")