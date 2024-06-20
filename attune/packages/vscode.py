from attune.packages.package_manager import PackageManager
from attune.vscode import vscode_subprocess


class VSCodePackageManager(PackageManager):
    def name(self):
        return "vscode"

    def _install_from_config(self, config):
        name = config["name"]

        id = self._get_install_config(config)["id"]

        self._install(name, id, None)

    def _install(self, name, id, args):
        vscode_subprocess(["--install-extension", id])

    def is_installed(self, package_name):
        return package_name in vscode_subprocess(["--list-extensions"])
