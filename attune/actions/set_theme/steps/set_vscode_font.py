from attune import features
from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.fonts import get_active_font_id, get_font_config
from attune.themes import get_theme_param
from attune.vscode import set_vscode_font


class SetVSCodeFontStep(SetThemeStep):
    @staticmethod
    def create():
        return SetVSCodeFontStep()

    def run(self, theme_name):
        if not features.is_enabled("VSCODE"):
            return
        code_font_id = get_active_font_id()
        if code_font_id is not None:
            font_config = get_font_config(code_font_id, validate=True)
            if font_config is not None:
                code_font_family = font_config.get("family")
                code_font_size = get_theme_param(theme_name, "code.font.size")
                print(
                    f"Seting vscode font to: '{code_font_id}', size = {code_font_size}"
                )
                set_vscode_font(code_font_family, code_font_size)
