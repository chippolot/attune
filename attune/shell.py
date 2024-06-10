from os import environ
from pathlib import Path


def get_shell_name():
    shell_path = environ["SHELL"]
    return Path(shell_path).stem


def get_profile_filename():
    shell_name = get_shell_name()
    if shell_name == "bash":
        return ".bash_profile"
    elif shell_name == "zsh":
        return ".zprofile"
    else:
        raise Exception(f"Unsupported shell: {shell_name}")
