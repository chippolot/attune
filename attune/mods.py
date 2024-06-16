import json
import os

from attune import gum


def init():
    module_name = gum.input(prompt="Enter a module name: ")
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
            open(os.path.join(attune_mod_files_dir, filename), "w")
            print(f"Created file: {filename}")

    prompt_mod_file(".shell_profile")
    prompt_mod_file(".gitconfig")
    prompt_mod_file(".aliases")

    # Write the config.json file
    config_path = os.path.join(base_dir, ".attune-module", "config.json")
    with open(config_path, "w", encoding="utf-8") as config_file:
        json.dump(config_content, config_file, indent=4)
        print(f"Created config file: {config_path}")

    print("Successfully initialized new module!")
