import json

from attune.config import get_repo_file_path


def get_fonts_config():
    fonts_path = get_repo_file_path("themes/fonts.json")
    try:
        with open(fonts_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {fonts_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {fonts_path}")


def get_font_config(font_id, validate=False):
    fonts = get_fonts_config()
    if not font_id in fonts:
        if validate:
            print(f"Invalid font id: {font_id}")
        return None
    return fonts[font_id]


def get_font_ids():
    fonts = get_fonts_config()
    return fonts.keys()
