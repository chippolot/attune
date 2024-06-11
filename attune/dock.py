import json
import subprocess


class Dock:
    def get_current_items(self):
        try:
            result = subprocess.run(
                ["dockutil", "--list", "--json"], check=True, stdout=subprocess.PIPE
            )
            dock_items = json.loads(result.stdout)
            current_apps = [
                item["path"] for item in dock_items if item["tile-type"] == "file-tile"
            ]
            return current_apps
        except subprocess.CalledProcessError as e:
            print(f"Failed to get current Dock items: {e}")
            return []

    def clear(self):
        try:
            subprocess.run(["dockutil", "--remove", "all", "--no-restart"], check=True)
            print("Successfully cleared the Dock.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clear the Dock: {e}")

    def pin_item(self, app_path):
        try:
            subprocess.run(["dockutil", "--add", app_path, "--no-restart"], check=True)
            print(f"Successfully pinned {app_path} to the Dock.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to pin {app_path} to the Dock: {e}")

    def restart(self):
        try:
            subprocess.run(["killall", "Dock"], check=True)
            print("Dock restarted to apply changes.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to restart the Dock: {e}")
