import json

from attune.config import Config
from attune.dict import get_dict_value
from attune.paths import get_repo_file_path


def get_themes_config():
    themes_path = get_repo_file_path("themes/themes.json")
    try:
        with open(themes_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {themes_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {themes_path}")


def get_theme_param(theme_name, path):
    themes = get_themes_config().get("themes")
    if theme_name not in themes:
        return None
    theme = themes[theme_name]
    value = get_dict_value(theme, path)
    if value is not None:
        return value
    else:
        defaults = get_themes_config().get("defaults", {})
        return get_dict_value(defaults, path)


def get_theme_names():
    themes = get_themes_config().get("themes")
    return list(themes.keys())


def list_themes():
    print("\nThemes:")
    for key in sorted(get_theme_names()):
        print("- " + key)


def get_active_theme_name():
    config = Config.load()
    return config.get("theme.active")


def set_active_theme_name(theme_name):
    config = Config.load()
    config.set("theme.active", theme_name)
    config.save()


def get_default_theme_name():
    config = Config.load()
    return config.get("theme.default")


def set_default_theme_name(theme_name):
    config = Config.load()
    config.set("theme.default", theme_name)
    config.save()


def active_theme():
    active_theme_name = get_active_theme_name()
    if active_theme_name is not None:
        print(f"Active Theme: {active_theme_name}")
    else:
        print("No active theme set")
