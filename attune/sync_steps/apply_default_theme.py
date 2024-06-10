from attune.sync_steps.sync_step import SyncStep
from attune.themes import get_active_theme_name, get_default_theme_name, set_theme


class SyncStepApplyDefaultTheme(SyncStep):
    @staticmethod
    def create():
        return SyncStepApplyDefaultTheme()

    def desc(self):
        return "Checking active theme"

    def run(self):
        if get_active_theme_name() is None:
            print("\nNo theme set. Setting default theme...")
            set_theme(get_default_theme_name())
