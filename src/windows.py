import ctypes
import os
import winreg

def set_wallpaper(image_path):
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
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
    
    if not result:
        raise ctypes.WinError()
    
def set_windows_mode(dark_mode):
    try:
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
        
        # Set the value to 0 to enable dark mode or 1 to enable light mode
        value = 0 if dark_mode else 1
        winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
        winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        
        # Close the registry key
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set Windows mode to {'dark' if dark_mode else 'light'}: {e}")