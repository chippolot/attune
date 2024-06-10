import os
import json

from attune.dict import *


def get_settings_path():
    return os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
        "settings.json",
    )


def get_settings():
    settings_path = get_settings_path()
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as file:
            settings = json.load(file)
    else:
        settings = {}
    return settings


def save_settings(settings):
    with open(get_settings_path(), "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def set_terminal_profile_param(path, value):
    if value == None:
        return

    settings_path = get_settings_path()
    if not os.path.exists(settings_path):
        print(f"Configuration file not found: {settings_path}")
        return

    # Update font settings in default profile
    settings = get_settings()
    profiles = settings.get("profiles", {})
    defaults = profiles.get("defaults", {})
    set_dict_value(defaults, path, value)
    save_settings(settings)


def set_terminal_theme(name, theme_path):
    settings = get_settings()

    # Install / Update the theme
    if theme_path != None:
        if not os.path.exists(theme_path):
            raise FileNotFoundError(f"The file {theme_path} does not exist.")

        with open(theme_path, "r", encoding="utf-8") as file:
            theme = json.load(file)

        # Update existing theme
        themes = settings.get("themes", [])
        theme_found = False
        for other_theme in themes:
            if "name" in other_theme and other_theme["name"] == name:
                other_theme.clear()
                other_theme.update(theme)
                theme_found = True
                break

        # Add new theme if none was found
        if not theme_found:
            themes.append(theme)

        save_settings(settings)

    # Set the theme
    settings["theme"] = name
    save_settings(settings)


def set_terminal_color_scheme(name, color_scheme_path):
    # Install / Update the scheme
    if color_scheme_path != None:
        if not os.path.exists(color_scheme_path):
            raise FileNotFoundError(f"The file {color_scheme_path} does not exist.")

        with open(color_scheme_path, "r", encoding="utf-8") as file:
            color_scheme = json.load(file)

        settings = get_settings()

        # Update existing scheme
        schemes = settings.get("schemes", [])
        scheme_found = False
        for other_scheme in schemes:
            if "name" in other_scheme and other_scheme["name"] == name:
                other_scheme.clear()
                other_scheme.update(color_scheme)
                scheme_found = True
                break

        # Add new scheme if none was found
        if not scheme_found:
            schemes.append(color_scheme)

        save_settings(settings)

    # Set the scheme
    set_terminal_profile_param("colorScheme", name)
