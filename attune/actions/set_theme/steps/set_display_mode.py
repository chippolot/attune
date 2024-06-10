import platform

from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.themes import get_theme_param

if platform.system() == "Windows":
    from attune.platforms.windows import set_display_mode
elif platform.system() == "Darwin":
    from attune.platforms.mac import set_display_mode


class SetDisplayModeStep(SetThemeStep):
    @staticmethod
    def create():
        return SetDisplayModeStep()

    def run(self, theme_name):
        display_mode = get_theme_param(theme_name, "display_mode")
        if display_mode is not None:
            if display_mode in ["light", "dark"]:
                print(f"Seting OS display mode to: '{display_mode}'")
                set_display_mode(display_mode == "dark")
            else:
                print(f"Invalid display mode: {display_mode}")
