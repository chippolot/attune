import os
import re

from attune.paths import get_attune_file_path, get_repo_file_path
from attune.shell import get_profile_filename, get_shell_name


def flatten_dict(d, parent_key="", sep="."):
    """
    Flattens a nested dictionary so that each key is a dot-delimited path to its value.

    Parameters:
    d (dict): The dictionary to flatten.
    parent_key (str): The base key to use for each key in the flattened dictionary.
    sep (str): The separator to use between keys.

    Returns:
    dict: The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def apply(s, config):
    replacements = {
        "paths.config": get_attune_file_path().replace("\\", "/"),
        "paths.repo": get_repo_file_path().replace("\\", "/"),
        "shell.name": get_shell_name(),
        "shell.profile_filename": get_profile_filename(),
    }

    # Flatten the user config into replacement paths
    config_replacements = flatten_dict(config, "config")
    replacements = {**replacements, **config_replacements}

    def replacer(match):
        token = match.group(1)
        if token not in replacements:
            print(f"!! Invalid template replacement token: {token}")
        replacement = replacements.get(token, match.group(0))
        if "~" in replacement:
            maybe_path = os.path.expanduser(replacement)
            if os.path.exists(maybe_path):
                replacement = maybe_path
        return replacement

    pattern = re.compile(r"{{(.*?)}}")
    result = pattern.sub(replacer, s)
    return result
