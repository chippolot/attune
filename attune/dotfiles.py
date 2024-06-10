import os
import re
from pathlib import Path
from enum import Enum
from attune.config import get_repo_file_path, get_attune_file_path


class DotfileSource(Enum):
    HOME = 1
    ATTUNE = 2
    REPO = 3


def get_or_create_dotfile_path(source: DotfileSource, filename):
    filepath = ""
    if source == DotfileSource.HOME:
        home_dir = os.path.expanduser("~")
        filepath = os.path.join(home_dir, filename)
    elif source == DotfileSource.ATTUNE:
        filepath = get_attune_file_path(filename)
    elif source == DotfileSource.REPO:
        filepath = get_repo_file_path(f"dotfiles/{filename}")
    else:
        raise ValueError(f"Unsupported dotfile source: {source}")
    if not os.path.exists(filepath):
        Path(filepath).touch()
    return filepath


def replace_dotfile_line(source: DotfileSource, filename, pattern, newline):
    filepath = get_or_create_dotfile_path(source, filename)

    # Read the file contents
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Compile the regex pattern
    regex = re.compile(pattern)

    # Check if the pattern exists and replace it if found
    pattern_found = False
    for i in range(len(lines)):
        if regex.search(lines[i]):
            lines[i] = newline
            pattern_found = True
            break

    # If the pattern was not found, append the newline
    if not pattern_found:
        lines.append(newline)

    # Write the updated contents back to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(lines)
