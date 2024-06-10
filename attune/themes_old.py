import os

from attune.config import get_or_create_config, save_config
from attune.paths import get_repo_file_path
from attune.terminal import (
    set_terminal_color_scheme,
    set_terminal_theme,
)
from attune.themes import (
    get_theme_param,
    set_terminal_theme_setting,
)


def set_theme(theme_name):
    # Set Terminal Color Scheme
    term_scheme_name = get_theme_param(theme_name, "terminal.color_scheme.name")
    if term_scheme_name is not None:
        print(f"Seting terminal color scheme to: {term_scheme_name}")
        term_scheme_file = get_theme_param(theme_name, "terminal.color_scheme.file")
        term_scheme_path = None
        if term_scheme_file is not None:
            term_scheme_path = get_repo_file_path(
                f"themes/terminal/windows/{term_scheme_file}", validate=True
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
                f"themes/terminal/windows/{term_theme_file}", validate=True
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
