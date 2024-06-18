import json
import os
import re
import shutil
from urllib.parse import urlparse

from attune import git, gum, template, utils
from attune.config import Config
from attune.packages.packages import get_package_manager
from attune.paths import get_attune_file_path, get_modules_file_path


class ModuleConfig:
    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as config_file:
            cfg = json.load(config_file)
            return cls(cfg)

    def __init__(self, cfg):
        self.cfg = cfg

    def name(self):
        return self.cfg.get("name", None)

    def id(self):
        return utils.snake_case(self.name())

    def dotfiles(self):
        return self.cfg.get("dotfiles", {})

    def packages(self):
        return self.cfg.get("packages", {})


def init():
    module_name = gum.write(placeholder="Enter a module name: ")
    module_desc = gum.write(placeholder="Enter a module description: ")
    base_dir = os.getcwd()

    # Define the directory structure
    attune_mod_dir = os.path.join(base_dir, ".attune-module")
    attune_mod_dotfiles_dir = os.path.join(attune_mod_dir, "dotfiles")
    directories = [
        base_dir,
        attune_mod_dir,
        attune_mod_dotfiles_dir,
    ]

    # Define a basic config.json content
    dotfiles = {}
    config_content = {
        "name": module_name,
        "description": module_desc,
        "dotfiles": dotfiles,
    }

    # Create the directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    def prompt_mod_file(filename):
        if gum.confirm(prompt=f"Should this mod contain a {filename} extension?"):
            dotfiles[filename] = f"dotfiles/{filename}"
            utils.touch(os.path.join(attune_mod_dotfiles_dir, filename))
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
    url = os.path.expanduser(url)

    config = Config.load()
    if __is_installed(url):
        print("Module is already installed.")
        return

    modules = config.get("modules", [])
    modules.append({"url": url, "local_dir": __get_local_module_folder_name(url)})
    config.set("modules", modules)

    sync(url)

    config.save()

    print(f"Installed module from '{url}'.")


def rebuild_dotfiles():
    combined_files = {}

    # Loop through all modules and collect the contents of each file
    config = Config.load()
    for module in get_installed_modules():
        path_to_module = get_local_path(module.get("url"))
        module_config = ModuleConfig.load(os.path.join(path_to_module, "config.json"))
        for filename, relative_file_path in module_config.dotfiles().items():
            full_file_path = os.path.join(path_to_module, relative_file_path)
            if filename not in combined_files:
                combined_files[filename] = ""
            dotfile_contents = utils.read_file(full_file_path)
            dotfile_contents = template.apply(dotfile_contents, config._cfg)
            combined_files[filename] += dotfile_contents + "\n\n"

    # Write the combined contents to the destination dotfiles
    for filename, content in combined_files.items():
        destination_path = get_attune_file_path(filename)
        with open(destination_path, "w", encoding="utf-8") as dest_file:
            dest_file.write(content)


def uninstall(url):
    url = os.path.expanduser(url)

    config = Config.load()
    if not __is_installed(url):
        print(f"Module with url '{url}' is not installed.")
        return

    path_to_module = get_local_base_path(url)
    if os.path.exists(path_to_module):
        shutil.rmtree(path_to_module)

    modules = config.get("modules", [])
    modules = [m for m in modules if m.get("url").casefold() != url.casefold()]
    config.set("modules", modules)
    config.save()

    print(f"Uninstalled module with url: '{url}'.")


def sync(url):
    path_to_module = get_local_base_path(url)

    # Update local module folder
    if __is_local(url):
        if os.path.exists(path_to_module):
            shutil.rmtree(path_to_module)
        shutil.copytree(url, path_to_module)
    elif __is_remote(url):
        if os.path.exists(path_to_module):
            git.pull(path_to_module)
        else:
            git.clone(url, path_to_module)
    else:
        raise Exception(f"Invalid module url: '{url}'.")

    # Apply module
    path_to_module = get_local_path(url)
    module_config = ModuleConfig.load(os.path.join(path_to_module, "config.json"))

    __install_packages(module_config)


def get_local_base_path(url):
    return os.path.join(get_modules_file_path(), __get_local_module_folder_name(url))


def get_local_path(url):
    base_path = get_local_base_path(url)
    for root, _, files in os.walk(base_path):
        if "config.json" in files:
            return root
    return None


def get_installed_modules():
    config = Config.load()
    return config.get("modules", [])


def __is_installed(url):
    for module in get_installed_modules():
        mod_url = module.get("url", None)
        if mod_url is not None and mod_url.casefold() == url.casefold():
            return True
    return False


def __get_local_module_folder_name(url):
    # Git URL pattern
    github_pattern = (
        r"(?:https?://|git@)(?:www\.)?github\.com[:/]([^/]+)/([^/]+)(?:\.git)?"
    )

    # Check if it's a github URL
    github_match = re.match(github_pattern, url)
    if github_match:
        user, repo = github_match.groups()
        return f"{user}@{repo.rstrip('.git')}"

    # If not a git URL, assume it's a local path
    if os.path.exists(url):
        config_path = os.path.join(url, "config.json")
        if os.path.exists(config_path):
            config = ModuleConfig.load(config_path)
            id = config.id()
            return f"local@{id}"
        else:
            raise Exception(
                f"Failed to locate config.json file in local attune module path: '{config_path}'."
            )

    # If no match or valid local path found
    return None


def __is_local(url):
    return os.path.exists(url)


def __is_remote(url):
    return urlparse(url).scheme in (
        "http",
        "https",
    )


def __install_packages(module_config):
    packages = module_config.packages()
    if len(packages) == 0:
        return

    print(f"Installing packages from module '{module_config.name()}'.")

    package_manager = get_package_manager()
    for package_config in packages:
        package_manager.install_from_config(package_config)
