#!/usr/bin/env python3

import argparse

from attune import gum
from attune.actions.set_theme.set_theme import set_theme
from attune.actions.sync.sync import sync
from attune.config import Config
from attune.fonts import get_font_ids, set_active_font_id
from attune.terminal.terminal import get_terminal
from attune.themes import get_active_theme_name, get_theme_names
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

    # Cmd: font
    subparser = subparsers.add_parser(
        "font", help="Selects a new attune font to apply system-wide."
    )
    subparser.set_defaults(func=font_cmd)

    # Cmd: mod
    mod_parser = subparsers.add_parser("mod", help="Manage modules")
    mod_subparsers = mod_parser.add_subparsers(
        title="mod commands",
        description="valid mod commands",
        help="additional mod commands help",
    )

    # Cmd: mod init
    mod_init_parser = mod_subparsers.add_parser(
        "init", help="Initialize a new module directory structure in a fresh repo"
    )
    mod_init_parser.set_defaults(func=init_module_cmd)

    # Cmd: mod install <git_url>
    mod_install_parser = mod_subparsers.add_parser(
        "install", help="Add a module from a git URL"
    )
    mod_install_parser.add_argument(
        "git_url", type=str, help="The git URL of the module to install"
    )
    mod_install_parser.set_defaults(func=install_module_cmd)

    # Cmd: mod uninstall <id>
    mod_uninstall_parser = mod_subparsers.add_parser(
        "uninstall", help="Remove a module by module ID"
    )
    mod_uninstall_parser.add_argument(
        "id", type=str, help="The ID of the module to uninstall"
    )
    mod_uninstall_parser.set_defaults(func=uninstall_module_cmd)

    # Cmd: config
    subparser = subparsers.add_parser(
        "config", help="Opens the user config file for editing."
    )
    subparser.set_defaults(func=edit_config_cmd)

    args = parser.parse_args()
    print(args)
    if "func" in args:
        args.func(args)
    elif args.command == "mod":
        mod_parser.print_help()
    else:
        parser.print_help()

    # Handle any queued requests
    terminal = get_terminal()
    if terminal.needs_restart:
        terminal.restart()


def sync_cmd(args):
    sync(reconfigure=args.reconfigure)


def theme_cmd(args):
    theme_name = gum.choose(get_theme_names(), header="Select a theme: ")
    if theme_name is None:
        return
    set_theme(theme_name)


def font_cmd(args):
    font_id = gum.choose(get_font_ids(), header="Select a font: ")
    if font_id is None:
        return
    set_active_font_id(font_id)
    set_theme(get_active_theme_name())


def edit_config_cmd(args):
    if not Config.exists():
        print("Cannot edit user config until sync has been run at least once!")
        return
    vscode_subprocess([Config.path()])


def init_module_cmd(args):
    # TODO Implement
    pass


def install_module_cmd(args):
    # TODO Implement
    pass


def uninstall_module_cmd(args):
    # TODO Implement
    pass


if __name__ == "__main__":
    main()
