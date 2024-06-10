import subprocess


class Terminal:
    def set_font(self, font_family, font_size):
        # TODO Implement
        pass

    def set_theme(self, name, theme_path):
        # TODO prevent new terminal from opening
        try:
            # Open the .terminal file to import the profile settings
            subprocess.run(["open", theme_path], check=True)

            # Use AppleScript to set the imported profile as the default
            apple_script = f"""
            tell application "Terminal"
                set default settings to settings set "{name}"
                set startup settings to settings set "{name}"
                set current settings of tabs of (every window whose visible is true) to settings set "{name}"
            end tell
            """
            subprocess.run(["osascript", "-e", apple_script], check=True)

            print(
                f"Applied terminal profile from '{theme_path}' and set it as default."
            )
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
