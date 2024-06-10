from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.themes import get_theme_param
from attune.vscode import set_vscode_theme


class SetVSCodeColorThemeStep(SetThemeStep):
    @staticmethod
    def create():
        return SetVSCodeColorThemeStep()

    def run(self, theme_name):
        code_theme_name = get_theme_param(theme_name, "code.color_theme.name")
        code_theme_ext = get_theme_param(theme_name, "code.color_theme.extension")
        if code_theme_name is not None:
            print(f"Seting vscode color theme to: '{code_theme_name}'")
            set_vscode_theme(code_theme_name, code_theme_ext)
