from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.fonts import get_font_config
from attune.terminal.terminal import get_terminal
from attune.themes import get_theme_param


class SetTerminalFontStep(SetThemeStep):
    @staticmethod
    def create():
        return SetTerminalFontStep()

    def run(self, theme_name):
        term_font_id = get_theme_param(theme_name, "terminal.font.id")
        if term_font_id is not None:
            font_config = get_font_config(term_font_id, validate=True)
            if font_config is not None:
                term_font_family = font_config.get("family")
                term_font_size = get_theme_param(theme_name, "terminal.font.size")
                print(
                    f"Seting terminal font to: '{term_font_id}', size = {term_font_size}"
                )
                get_terminal().set_font(term_font_family, term_font_size)
