#!/usr/bin/env python3

import argparse

from attune.config import edit_config
from attune.sync import sync
from attune.themes import active_theme, list_themes, set_theme


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to sync programming environments and themes."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Theme subcommand with its own subcommands
    parser_theme = subparsers.add_parser("theme", help="Manage themes")
    theme_subparsers = parser_theme.add_subparsers(dest="theme_command")

    parser_theme_list = theme_subparsers.add_parser(
        "list", help="List all available themes"
    )
    parser_theme_list.set_defaults(func=list_themes)

    parser_theme_set = theme_subparsers.add_parser("set", help="Set a theme as active")
    parser_theme_set.add_argument(
        "theme_name", type=str, help="The name of the theme to set as active"
    )
    parser_theme_set.set_defaults(func=set_theme)

    parser_theme_active = theme_subparsers.add_parser(
        "active", help="Show the active theme"
    )
    parser_theme_active.set_defaults(func=active_theme)

    # Sync subcommand
    parser_sync = subparsers.add_parser("sync", help="Sync the application")
    parser_sync.set_defaults(func=sync)

    # Config subcommand
    parser_config = subparsers.add_parser(
        "config", help="Opens the user config file for editing"
    )
    parser_config.set_defaults(func=edit_config)

    args = parser.parse_args()
    if args.command == "theme" and args.theme_command is None:
        parser_theme.print_help()
    elif hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
