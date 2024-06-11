import platform

from attune.actions.sync.steps.sync_step import SyncStep

if platform.system() == "Darwin":
    from attune.dock import Dock


class FilterDockAppsStep(SyncStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return None
        elif platform.system() == "Darwin":
            return MacFilterDockAppsStep()
        else:
            raise Exception("Unsupported platform")

    def desc(self):
        return "Setting dock apps"

    def run(self):
        pass


class MacFilterDockAppsStep(FilterDockAppsStep):
    def run(self):
        # TODO Do not restart if nothing changed!
        # TODO Set dock attributes (size, animate, etc)

        dock = Dock()
        desired_apps = [
            "/System/Applications/Utilities/Terminal.app",
            "/Applications/Visual Studio Code.app",
            "/Applications/Google Chrome.app",
            "~/Downloads",
            "/System/Applications/System Settings.app",
        ]

        # Clear the Dock
        dock.clear()

        # Pin specified applications to the Dock
        for app in desired_apps:
            dock.pin_item(app)

        # Restart the Dock to apply changes
        dock.restart()
