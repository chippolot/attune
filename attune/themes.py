import argparse
import json
import os

from attune.config import get_or_create_config, save_config
from attune.dict import get_dict_value
from attune.fonts import get_font_config
from attune.paths import get_repo_file_path
from attune.prompt import set_prompt_theme
from attune.terminal import (
    set_terminal_color_scheme,
    set_terminal_profile_param,
    set_terminal_theme,
)
from attune.vscode import set_vscode_font, set_vscode_theme
from attune.windows import set_wallpaper, set_windows_mode


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
    return themes.keys()


def list_themes(args):
    print("\nThemes:")
    for key in sorted(get_theme_names()):
        print("- " + key)


def set_theme(args):
    if isinstance(args, argparse.Namespace):
        theme_name = args.theme_name
    else:
        theme_name = args

    # Validate theme name and get config
    if theme_name not in get_theme_names():
        print(f"Invalid theme name: {theme_name}")
        list_themes(None)
        return

    # Set Background
    background_file = get_theme_param(theme_name, "background")
    if background_file is not None:
        print(f"Seting desktop background to: '{background_file}'")
        background_path = get_repo_file_path(
            f"themes/backgrounds/{background_file}", validate=True
        )
        set_wallpaper(background_path)

    # Set Display Mode
    display_mode = get_theme_param(theme_name, "display_mode")
    if display_mode is not None:
        if display_mode in ["light", "dark"]:
            print(f"Seting OS display mode to: '{display_mode}'")
            set_windows_mode(display_mode == "dark")
        else:
            print(f"Invalid display mode: {display_mode}")

    # Set Oh My Posh Theme
    prompt_file = get_theme_param(theme_name, "prompt")
    if prompt_file is not None:
        print(f"Seting oh-my-posh prompt theme to: '{prompt_file}'")
        prompt_path = os.path.abspath(
            get_repo_file_path(f"themes/prompts/{prompt_file}", validate=True)
        )
        set_prompt_theme(prompt_path)

    # Set VSCode Color Theme
    code_theme_name = get_theme_param(theme_name, "code.color_theme.name")
    code_theme_ext = get_theme_param(theme_name, "code.color_theme.extension")
    if code_theme_name is not None:
        print(f"Seting vscode color theme to: '{code_theme_name}'")
        set_vscode_theme(code_theme_name, code_theme_ext)

    # Set VSCode Font
    code_font_id = get_theme_param(theme_name, "code.font.id")
    if code_font_id is not None:
        font_config = get_font_config(code_font_id, validate=True)
        if font_config is not None:
            code_font_family = font_config.get("family")
            code_font_size = get_theme_param(theme_name, "code.font.size")
            print(f"Seting vscode font to: '{code_font_id}', size = {code_font_size}")
            set_vscode_font(code_font_family, code_font_size)

    # Set Terminal Font
    term_font_id = get_theme_param(theme_name, "terminal.font.id")
    if term_font_id is not None:
        font_config = get_font_config(term_font_id, validate=True)
        if font_config is not None:
            term_font_family = font_config.get("family")
            term_font_size = get_theme_param(theme_name, "terminal.font.size")
            print(f"Seting terminal font to: '{term_font_id}', size = {term_font_size}")
            set_terminal_profile_param("font.face", term_font_family)
            set_terminal_profile_param("font.size", term_font_size)

    # Set Terminal Color Scheme
    term_scheme_name = get_theme_param(theme_name, "terminal.color_scheme.name")
    if term_scheme_name is not None:
        print(f"Seting terminal color scheme to: {term_scheme_name}")
        term_scheme_file = get_theme_param(theme_name, "terminal.color_scheme.file")
        term_scheme_path = None
        if term_scheme_file is not None:
            term_scheme_path = get_repo_file_path(
                f"themes/terminal/{term_scheme_file}", validate=True
            )
        set_terminal_color_scheme(term_scheme_name, term_scheme_path)

    # Set Terminal Theme
    term_theme_name = get_theme_param(theme_name, "terminal.theme.name")
    if term_theme_name is not None:
        print(f"Seting terminal theme to: {term_theme_name}")
        term_theme_file = get_theme_param(theme_name, "terminal.theme.file")
        term_theme_path = None
        if term_theme_file is not None:
            term_theme_path = get_repo_file_path(
                f"themes/terminal/{term_theme_file}", validate=True
            )
        set_terminal_theme(term_theme_name, term_theme_path)

    # Set Other Terminal Params
    set_terminal_theme_setting("opacity", theme_name, "terminal.opacity")
    set_terminal_theme_setting("useAcrylic", theme_name, "terminal.useAcrylic")
    set_terminal_theme_setting("cursorShape", theme_name, "terminal.cursorShape")

    # Set active theme name and save config
    config = get_or_create_config()
    if "theme" not in config:
        config["theme"] = {}
    config["theme"]["active"] = theme_name
    save_config(config)

    os.system("cls" if os.name == "nt" else "clear")
    print(f"Set active theme to: {theme_name}\n")
    return


def get_active_theme_name():
    config = get_or_create_config()
    if "theme" in config:
        theme = config["theme"]
        if "active" in theme:
            return theme["active"]
    return None


def get_default_theme_name():
    config = get_or_create_config()
    if "theme" in config:
        theme = config["theme"]
        if "default" in theme:
            return theme["default"]
    return None


def active_theme(args):
    active_theme_name = get_active_theme_name()
    if active_theme_name is not None:
        print(f"Active Theme: {active_theme_name}")
    else:
        print("No active theme set")


def set_terminal_theme_setting(terminal_param_path, theme_name, config_param_path):
    value = get_theme_param(theme_name, config_param_path)
    if value is None:
        return
    print(f"Seting terminal parameter {terminal_param_path} to: {value}")
    set_terminal_profile_param(terminal_param_path, value)
