import subprocess


class Terminal:
    def set_font(self, font_family, font_size):
        # AppleScript to set the font in Terminal
        apple_script = f"""
        tell application "Terminal"
            set font name of window 1 to "{font_family}"
            set font size of window 1 to {font_size}
        end tell
        """

        try:
            # Run the AppleScript command using osascript
            subprocess.run(["osascript", "-e", apple_script], check=True)
            print(f"Terminal font set to {font_family} at size {font_size}.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
