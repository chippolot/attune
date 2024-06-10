import json
import os


class Terminal:
    def set_font(self, font_family, font_size):
        self.__set_profile_param("font.face", font_family)
        self.__set_profile_param("font.size", font_size)

    def __set_profile_param(self, path, value):
        if value is None:
            return

        settings_path = self.__get_settings_path()
        if not os.path.exists(settings_path):
            print(f"Configuration file not found: {settings_path}")
            return

        # Update font settings in default profile
        settings = self.__get_settings()
        profiles = settings.get("profiles", {})
        defaults = profiles.get("defaults", {})
        self.__set_dict_value(defaults, path, value)
        self.__save_settings(settings)

    def __get_settings_path(self):
        return os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Local",
            "Packages",
            "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
            "LocalState",
            "settings.json",
        )

    def __get_settings(self):
        settings_path = self.__get_settings_path()
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as file:
                settings = json.load(file)
        else:
            settings = {}
        return settings

    def __save_settings(self, settings):
        with open(self.__get_settings_path(), "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)
