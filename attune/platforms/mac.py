import os
import subprocess



def is_font_installed(font_family):
    try:
        # Run the fc-list command to check installed fonts
        result = subprocess.run(
            ["fc-list", ":family"], capture_output=True, text=True, check=True
        )

        # Check the output
        fonts = result.stdout.strip().split("\n")
        for font in fonts:
            if font_family.lower() in font.lower():
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False


def set_background(image_path):
    # Absolute path to the image
    image_path = os.path.abspath(image_path)

    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    # AppleScript command to set the desktop background
    apple_script = f'''
    tell application "System Events"
        set picture of every desktop to "{image_path}"
    end tell
    '''

    try:
        # Run the AppleScript command using osascript
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print("Desktop background set successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def set_display_mode(dark_mode):
    # AppleScript command to set the appearance to dark or light mode
    if dark_mode:
        apple_script = 'tell application "System Events" to tell appearance preferences to set dark mode to true'
    else:
        apple_script = 'tell application "System Events" to tell appearance preferences to set dark mode to false'

    try:
        # Run the AppleScript command using osascript
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print(f"Display mode set to {'dark' if dark_mode else 'light'} mode successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")