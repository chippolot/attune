from attune.actions.set_theme.set_theme import set_theme
from attune.actions.sync.steps.sync_step import SyncStep
from attune.fonts import get_active_font_id, get_default_font_id, set_active_font_id
from attune.themes import get_active_theme_name, get_default_theme_name


class ApplyDefaultThemeStep(SyncStep):
    @staticmethod
    def create():
        return ApplyDefaultThemeStep()

    def desc(self):
        return "Checking active theme"

    def run(self):
        old_theme_name = get_active_theme_name()
        theme_name = old_theme_name or get_default_theme_name()

        old_font_id = get_active_font_id()
        font_id = old_font_id or get_default_font_id()

        if old_theme_name != theme_name or old_font_id != font_id:
            set_active_font_id(font_id)
            print(f"Updating theme to {theme_name} and font to {font_id}...")
            set_theme(theme_name)
        else:
            print("Theme and font are already set.")
