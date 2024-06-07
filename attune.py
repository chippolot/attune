#!/usr/bin/env python3

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sync import sync

def theme(args):
    print(f"Applying theme: {args.theme_name}")

def list_themes(args):
    print("Listing themes...")

def main():
    parser = argparse.ArgumentParser(description="A CLI tool to sync programming environments and themes.")
    subparsers = parser.add_subparsers(dest="command")

    # Theme subcommand
    parser_theme = subparsers.add_parser('theme', help="Apply a theme")
    parser_theme.add_argument('theme_name', type=str, help="The name of the theme to apply")
    parser_theme.set_defaults(func=theme)

    # List Themes subcommand
    parser_list_themes = subparsers.add_parser('list-themes', help="Lists all themes")
    parser_list_themes.set_defaults(func=list_themes)

    # Sync subcommand
    parser_sync = subparsers.add_parser('sync', help="Sync the application")
    parser_sync.set_defaults(func=sync)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()