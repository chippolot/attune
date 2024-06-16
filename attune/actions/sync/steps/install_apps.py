from attune.actions.sync.steps.sync_step import SyncStep
from attune.packages.packages import get_package_manager, get_packages_config


class InstallAppsStep(SyncStep):
    @staticmethod
    def create():
        return InstallAppsStep()

    def desc(self):
        return "Checking app dependencies"

    def run(self):
        package_manager = get_package_manager()
        packages_config = get_packages_config()
        for config in packages_config:
            package_manager.install_from_config(config)
