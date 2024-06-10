import os
import platform

from attune.config import get_or_create_config, save_config
from attune.fonts import get_font_config
from attune.paths import get_repo_file_path
from attune.terminal import (
    set_terminal_color_scheme,
    set_terminal_profile_param,
    set_terminal_theme,
)
from attune.themes import (
    get_theme_param,
    set_terminal_theme_setting,
)

if platform.system() == "Windows":
    pass


def set_theme(theme_name):
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
