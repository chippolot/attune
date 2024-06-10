import ctypes
import os
import subprocess
import time
import winreg


def set_background(image_path):
    # Absolute path to the image
    image_path = os.path.abspath(image_path)

    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    # SystemParametersInfo constants
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDWININICHANGE = 2

    # Call SystemParametersInfo to set the wallpaper
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )

    if not result:
        raise ctypes.WinError()


def set_display_mode(dark_mode):
    try:
        # Function to set the theme mode in the registry
        def set_mode(value):
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                0,
                winreg.KEY_SET_VALUE,
            )
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)

        # Toggle theme mode to force UI refresh
        set_mode(0 if dark_mode else 1)

        # Broadcast a WM_SETTINGCHANGE message to update the UI
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002

        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "ImmersiveColorSet",
            SMTO_ABORTIFHUNG,
            100,
            ctypes.byref(ctypes.c_ulong()),
        )

        # Restart Windows Explorer to apply changes across all monitors
        subprocess.run(
            ["taskkill", "/F", "/IM", "explorer.exe"],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        time.sleep(0.25)  # Short delay to ensure Explorer process is killed
        subprocess.run(
            ["start", "explorer.exe"], shell=True, check=True, stdout=subprocess.DEVNULL
        )

    except Exception as e:
        print(f"Failed to set Windows mode to {'dark' if dark_mode else 'light'}: {e}")


def is_font_installed(font_family):
    # PowerShell command to check installed fonts
    ps_command = f"""
    [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null
    $fonts = (New-Object System.Drawing.Text.InstalledFontCollection).Families
    $font_names = $fonts | ForEach-Object {{ $_.Name }}
    $font_names -contains '{font_family}'
    """

    try:
        # Run the PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", ps_command], capture_output=True, text=True
        )

        # Check the output
        output = result.stdout.strip()
        if output.lower() == "true":
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False
