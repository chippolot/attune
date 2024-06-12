#!/usr/bin/env python3

import argparse

from attune import gum
from attune.actions.set_theme.set_theme import set_theme
from attune.actions.sync.sync import sync
from attune.config import edit_config
from attune.themes import active_theme, get_theme_names


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to sync programming environments and themes."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Theme subcommand with its own subcommands
    parser_theme = subparsers.add_parser("theme", help="Manage themes")
    theme_subparsers = parser_theme.add_subparsers(dest="theme_command")

    parser_theme_set = theme_subparsers.add_parser("set", help="Set a theme as active")
    parser_theme_set.add_argument(
        "theme_name",
        type=str,
        default=None,
        nargs="?",
        help="The name of the theme to set as active",
    )
    parser_theme_set.set_defaults(func=set_theme_cmd)

    parser_theme_active = theme_subparsers.add_parser(
        "active", help="Show the active theme"
    )
    parser_theme_active.set_defaults(func=active_theme_cmd)

    # Sync subcommand
    parser_sync = subparsers.add_parser("sync", help="Sync the application")
    parser_sync.set_defaults(func=sync_cmd)

    # Config subcommand
    parser_config = subparsers.add_parser(
        "config", help="Opens the user config file for editing"
    )
    parser_config.set_defaults(func=edit_config_cmd)

    args = parser.parse_args()
    if args.command == "theme" and args.theme_command is None:
        parser_theme.print_help()
    elif hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def set_theme_cmd(args):
    theme_name = args.theme_name
    if theme_name is None:
        theme_name = gum.choose(get_theme_names())
    set_theme(theme_name)


def edit_config_cmd(args):
    edit_config()


def sync_cmd(args):
    sync()


def active_theme_cmd(args):
    active_theme()


if __name__ == "__main__":
    main()
