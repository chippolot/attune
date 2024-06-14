#!/usr/bin/env python3

import argparse

from attune import gum
from attune.actions.set_theme.set_theme import set_theme
from attune.actions.sync.sync import sync
from attune.config import Config
from attune.themes import get_theme_names
from attune.vscode import vscode_subprocess


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to sync programming environments and themes."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Cmd: sync
    subparser = subparsers.add_parser(
        "sync", help="Syncs attune scripts and runs attune."
    )
    subparser.add_argument(
        "-r",
        "--reconfigure",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Shows attune configuration wizard during sync.",
    )
    subparser.set_defaults(func=sync_cmd)

    # Cmd: theme
    subparser = subparsers.add_parser(
        "theme", help="Selects a new attune theme to apply system-wide."
    )
    subparser.set_defaults(func=theme_cmd)

    # Cmd: config
    subparser = subparsers.add_parser(
        "config", help="Opens the user config file for editing."
    )
    subparser.set_defaults(func=edit_config_cmd)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def sync_cmd(args):
    sync(reconfigure=args.reconfigure)


def theme_cmd(args):
    theme_name = gum.choose(get_theme_names())
    if theme_name is None:
        return
    set_theme(theme_name)


def edit_config_cmd(args):
    if not Config.exists():
        print("Cannot edit user config until sync has been run at least once!")
        return
    vscode_subprocess([Config.path()])


if __name__ == "__main__":
    main()
