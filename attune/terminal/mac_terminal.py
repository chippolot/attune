import subprocess
from pathlib import Path


class Terminal:
    def set_font(self, font_family, font_size):
        # TODO settings are copied??
        # TODO font sizes don't update immediately
        applescript = f"""
        set newFontFamily to "{font_family}"
        set newFontSize to {font_size}

        tell application "Terminal"
            set DefaultSettingsName to name of default settings
            set font name of default settings to newFontFamily
            set font size of default settings to newFontSize

            -- Apply the settings to all open Terminal windows
            set current settings of tabs of (every window whose visible is true) to settings set DefaultSettingsName
        end tell
        """

        # Run the AppleScript using osascript
        subprocess.run(["osascript", "-e", applescript], check=True)

    def set_theme(self, name, theme_path):
        # TODO prevent new terminal from opening
        try:
            # Open the .terminal file to import the profile settings
            subprocess.run(["open", theme_path], check=True)

            name = Path(theme_path).stem

            # Use AppleScript to set the imported profile as the default
            apple_script = f"""
            tell application "Terminal"
                set default settings to settings set "{name}"
                set startup settings to settings set "{name}"
                set current settings of tabs of (every window whose visible is true) to settings set "{name}"
            end tell
            """
            subprocess.run(["osascript", "-e", apple_script], check=True)

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
