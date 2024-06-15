import json
import os

from attune.dict import set_dict_value
from attune.themes import get_theme_param


class Terminal:
    needs_restart = False

    def set_font(self, font_family, font_ps, font_size):
        self.__set_profile_param("font.face", font_family)
        self.__set_profile_param("font.size", font_size)

    def set_theme(self, name, theme_path):
        settings = self.__get_settings()

        # Install / Update the theme
        if theme_path is not None:
            if not os.path.exists(theme_path):
                raise FileNotFoundError(f"The file {theme_path} does not exist.")

            with open(theme_path, "r", encoding="utf-8") as file:
                theme = json.load(file)

            # Update existing theme
            themes = settings.get("themes", [])
            theme_found = False
            for other_theme in themes:
                if "name" in other_theme and other_theme["name"] == name:
                    other_theme.clear()
                    other_theme.update(theme)
                    theme_found = True
                    break

            # Add new theme if none was found
            if not theme_found:
                themes.append(theme)

            self.__save_settings(settings)

        # Set the theme
        settings["theme"] = name
        self.__save_settings(settings)

    def set_color_scheme(self, name, color_scheme_path):
        # Install / Update the scheme
        if color_scheme_path is not None:
            if not os.path.exists(color_scheme_path):
                raise FileNotFoundError(f"The file {color_scheme_path} does not exist.")

            with open(color_scheme_path, "r", encoding="utf-8") as file:
                color_scheme = json.load(file)

            settings = self.__get_settings()

            # Update existing scheme
            schemes = settings.get("schemes", [])
            scheme_found = False
            for other_scheme in schemes:
                if "name" in other_scheme and other_scheme["name"] == name:
                    other_scheme.clear()
                    other_scheme.update(color_scheme)
                    scheme_found = True
                    break

            # Add new scheme if none was found
            if not scheme_found:
                schemes.append(color_scheme)

            self.__save_settings(settings)

        # Set the scheme
        self.__set_profile_param("colorScheme", name)

    def set_theme_setting(self, terminal_param_path, theme_name, config_param_path):
        value = get_theme_param(theme_name, config_param_path)
        if value is None:
            return
        print(f"Seting terminal parameter {terminal_param_path} to: {value}")
        self.__set_profile_param(terminal_param_path, value)

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
        set_dict_value(defaults, path, value)
        self.__save_settings(settings)

    def __save_settings(self, settings):
        with open(self.__get_settings_path(), "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)
