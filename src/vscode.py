import os
import json
import subprocess


def get_settings_path():
    path = os.path.join(
        os.path.expanduser("~"), "AppData", "Roaming", "Code", "User", "settings.json"
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_settings():
    settings_path = get_settings_path()
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as file:
            settings = json.load(file)
    else:
        settings = {}
    return settings


def save_settings(settings):
    with open(get_settings_path(), "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def install_vscode_extension(extension_name):
    try:
        # Use the 'code' command to install the extension
        result = subprocess.run(
            ["code.cmd", "--install-extension", extension_name],
            check=True,
            text=True,
            capture_output=True,
        )
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install VSCode extension {extension_name}: {e}")


def set_vscode_theme(theme_name, extension_name=None):
    # If an extension name is provided, install it first
    if extension_name:
        install_vscode_extension(extension_name)

    # Set the color theme
    settings = get_settings()
    settings["workbench.colorTheme"] = theme_name
    save_settings(settings)


def set_vscode_font(font_family, font_size):
    # Ensure font family and size are provided
    if not font_family or not font_size:
        print("Font family and size must be provided.")
        return

    # Set the editor font family and size
    settings = get_settings()
    settings["editor.fontFamily"] = font_family
    settings["editor.fontSize"] = font_size
    save_settings(settings)
