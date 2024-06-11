import os
import plistlib
import subprocess
import sys
import time
from pathlib import Path

from attune.themes import get_theme_param


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
        self._restart()

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

        defaultTheme = plist_data["New Bookmarks"][0]

        for key, value in theme_data.items():
            defaultTheme[key] = value
            defaultTheme[key + " (Light)"] = value
            defaultTheme[key + " (Dark)"] = value

        plist_data[color_preset_key][theme_name] = theme_data
        defaultTheme["Dynamic Profiles"] = theme_name

        value = get_theme_param(theme_name, "terminal.opacity")
        if value is not None:
            defaultTheme["Transparency"] = 1.0 - (value / 100.0)

        # Write the updated plist back to the file
        with open(plist_path, "wb") as f:
            plistlib.dump(plist_data, f)

        # Restart iTerm2 to apply the changes
        self._restart()

    def _restart(self):
        # Fork a child process
        pid = os.fork()
        if pid > 0:
            # Parent process exits immediately
            sys.exit()
        else:
            # Child process continues
            # Create a new session to detach from the terminal
            os.setsid()

            # Fork again to ensure the process is re-parented to init (PID 1)
            pid = os.fork()
            if pid > 0:
                # First child process exits
                sys.exit()
            else:
                # Second child process continues
                # Wait a moment to ensure the parent terminal is detached
                time.sleep(0.75)

                # Kill iTerm2
                subprocess.run(["pkill", "iTerm2"])

                # Wait for a moment to ensure the process is terminated
                time.sleep(1)

                # Restart iTerm2
                subprocess.run(["open", "-a", "iTerm"])
