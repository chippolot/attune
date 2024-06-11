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

    # Ensure the path to PlistBuddy
    plist_buddy_path = "/usr/libexec/PlistBuddy"

    # Ensure the path to the plist file
    plist_path = os.path.expanduser(
        "~/Library/Application Support/com.apple.wallpaper/Store/Index.plist"
    )

    # Construct the command to set the new wallpaper path
    plist_buddy_command = f'{plist_buddy_path} -c "set AllSpacesAndDisplays:Desktop:Content:Choices:0:Files:0:relative file://{image_path}" "{plist_path}"'

    # Construct the command to restart WallpaperAgent
    kill_wallpaper_agent_command = "killall WallpaperAgent"

    try:
        subprocess.run(plist_buddy_command, shell=True, check=True)
        subprocess.run(kill_wallpaper_agent_command, shell=True, check=True)

    except subprocess.CalledProcessError:
        raise Exception(
            "Failed to set desktop wallpaper.\nGo to System Settings > Wallpaper and toggle 'Show on all Spaces' and try again."
        )


def set_display_mode(dark_mode):
    # AppleScript command to set the appearance to dark or light mode
    if dark_mode:
        apple_script = 'tell application "System Events" to tell appearance preferences to set dark mode to true'
    else:
        apple_script = 'tell application "System Events" to tell appearance preferences to set dark mode to false'

    try:
        # Run the AppleScript command using osascript
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print(
            f"Display mode set to {'dark' if dark_mode else 'light'} mode successfully."
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
