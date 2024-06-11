from attune.actions.set_theme.set_theme import set_theme
from attune.actions.sync.steps.sync_step import SyncStep
from attune.themes import get_active_theme_name, get_default_theme_name


class ApplyDefaultThemeStep(SyncStep):
    @staticmethod
    def create():
        return ApplyDefaultThemeStep()

    def desc(self):
        return "Checking active theme"

    def run(self):
        if get_active_theme_name() is None:
            print("No theme set. Setting default theme...")
            set_theme(get_default_theme_name())
        else:
            print("Theme already set.")
