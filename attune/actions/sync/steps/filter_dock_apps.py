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
        return "Updating system settings"

    def run(self):
        pass


class MacFilterDockAppsStep(FilterDockAppsStep):
    def run(self):
        dock = Dock()
        keep_apps = [
            "Finder",
            "Terminal",
            "Visual Studio Code",
            "Google Chrome",
            "System Preferences",
        ]

        # Load current Dock preferences
        dock_plist = dock.load_plist()

        # Filter out unwanted apps
        original_apps = dock_plist.get("persistent-apps", [])
        filtered_apps = dock.filter_apps(dock_plist, keep_apps)

        # Check if the app list has changed
        if original_apps != filtered_apps:
            dock_plist["persistent-apps"] = filtered_apps

            # Save the modified preferences back to the plist file
            dock.save_plist(dock_plist)

            # Restart the Dock to apply changes
            dock.restart()
            print("Dock restarted with updated app list.")
        else:
            print("No changes to the Dock app list.")
