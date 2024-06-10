import os


def get_repo_file_path(relative_path="", validate=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "../", relative_path)
    path = os.path.abspath(path)
    if validate and not os.path.exists(path):
        raise Exception(f"Invalid file path: {path}")
    return path


def get_attune_file_path(relative_path=""):
    home_dir = os.path.expanduser("~")
    attune_path = os.path.join(home_dir, ".attune")
    if not os.path.exists(attune_path):
        os.makedirs(attune_path)
    return os.path.join(attune_path, relative_path)
