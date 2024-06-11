import os
import plistlib
import subprocess
import time
from pathlib import Path


class Terminal:
    def set_font(self, font_family, font_ps, font_size):
        plist_path = os.path.expanduser(
            "~/Library/Preferences/com.googlecode.iterm2.plist"
        )

        if not Path(plist_path).exists():
            raise FileNotFoundError(
                f"{plist_path} does not exist. Ensure iTerm2 is installed and has been run at least once."
            )

        # Read the existing plist
        with open(plist_path, "rb") as f:
            plist_data = plistlib.load(f)

        # Modify the font settings
        plist_data["New Bookmarks"][0]["Normal Font"] = f"{font_ps} {font_size}"
        plist_data["New Bookmarks"][0]["Non Ascii Font"] = f"{font_ps} {font_size}"

        # Write the updated plist back to the file
        with open(plist_path, "wb") as f:
            plistlib.dump(plist_data, f)

        # Restart iTerm2 to apply the changes
        self._restart_iterm2()

    def set_theme(self, name, theme_path):
        plist_path = os.path.expanduser(
            "~/Library/Preferences/com.googlecode.iterm2.plist"
        )

        if not Path(plist_path).exists():
            raise FileNotFoundError(
                f"{plist_path} does not exist. Ensure iTerm2 is installed and has been run at least once."
            )

        # Read the existing plist
        with open(plist_path, "rb") as f:
            plist_data = plistlib.load(f)

        # Modify the color scheme settings
        theme_name = Path(theme_path).stem
        color_preset_key = "Custom Color Presets"
        if color_preset_key not in plist_data:
            plist_data[color_preset_key] = {}

        # Assuming the theme file is another plist that needs to be read
        with open(theme_path, "rb") as f:
            theme_data = plistlib.load(f)

        for key, value in theme_data.items():
            plist_data["New Bookmarks"][0][key] = value
            plist_data["New Bookmarks"][0][key + " (Light)"] = value
            plist_data["New Bookmarks"][0][key + " (Dark)"] = value

        plist_data[color_preset_key][theme_name] = theme_data
        plist_data["New Bookmarks"][0]["Dynamic Profiles"] = theme_name

        # Write the updated plist back to the file
        with open(plist_path, "wb") as f:
            plistlib.dump(plist_data, f)

        # Restart iTerm2 to apply the changes
        self._restart_iterm2()

    def _restart_iterm2(self):
        # Kill iTerm2 if it is running
        subprocess.run(["killall", "iTerm2"], stderr=subprocess.DEVNULL, check=False)
        # Wait for a moment to ensure iTerm2 is closed
        time.sleep(2)
        # Open iTerm2
        subprocess.run(["open", "-a", "iTerm"])
