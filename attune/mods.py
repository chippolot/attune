import json
import os

from attune import gum, utils
from attune.config import Config


def init():
    module_name = gum.write(placeholder="Enter a module name: ")
    module_desc = gum.write(placeholder="Enter a module description: ")
    base_dir = os.getcwd()

    # Define the directory structure
    attune_mod_dir = os.path.join(base_dir, ".attune-module")
    attune_mod_files_dir = os.path.join(attune_mod_dir, "files")
    directories = [
        base_dir,
        attune_mod_dir,
        attune_mod_files_dir,
    ]

    # Define a basic config.json content
    files = {}
    config_content = {
        "name": module_name,
        "description": module_desc,
        "files": files,
    }

    # Create the directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    def prompt_mod_file(filename):
        if gum.confirm(prompt=f"Should this mod contain a {filename} extension?"):
            files[filename] = f"files/{filename}"
            utils.touch(os.path.join(attune_mod_files_dir, filename))
            print(f"Created file: {filename}")

    prompt_mod_file(".shell_profile")
    prompt_mod_file(".bash_profile")
    prompt_mod_file(".zprofile")
    prompt_mod_file(".gitconfig")
    prompt_mod_file(".aliases")

    # Write the config.json file
    config_path = os.path.join(base_dir, ".attune-module", "config.json")
    with open(config_path, "w", encoding="utf-8") as config_file:
        json.dump(config_content, config_file, indent=4)
        print(f"Created config file: {config_path}")

    print("Successfully initialized new module!")


def install(url):
    config = Config.load()
    if __is_installed(config, url):
        print("Module is already installed.")

    modules = config.get("modules", [])
    # TODO Add module here
    config["modules"] = modules
    print(f"Installed module from '{url}'.")


def __is_installed(config, url):
    for module in config.get("modules", []):
        mod_url = module.get("url", None)
        if mod_url is not None and mod_url.casefold() == url.casefold():
            return True
    return False
