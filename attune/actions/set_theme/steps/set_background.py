import platform

from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.paths import get_repo_file_path
from attune.themes import get_theme_param

if platform.system() == "Windows":
    from attune.platforms.windows import set_background
elif platform.system() == "Darwin":
    from attune.platforms.mac import set_background


class SetBackgroundStep(SetThemeStep):
    @staticmethod
    def create():
        return SetBackgroundStep()

    def run(self, theme_name):
        background_file = get_theme_param(theme_name, "background")
        if background_file is not None:
            print(f"Seting desktop background to: '{background_file}'")
            background_path = get_repo_file_path(
                f"themes/backgrounds/{background_file}", validate=True
            )
            set_background(background_path)
