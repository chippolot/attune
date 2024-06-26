from attune.actions.sync.steps.apply_default_theme import ApplyDefaultThemeStep
from attune.actions.sync.steps.configure_attune import ConfigureAttuneStep
from attune.actions.sync.steps.filter_dock_apps import FilterDockAppsStep
from attune.actions.sync.steps.git_pull import GitPullStep
from attune.actions.sync.steps.install_fonts import InstallFontsStep
from attune.actions.sync.steps.install_gum import InstallGumStep
from attune.actions.sync.steps.patch_dotfiles import PatchDotfilesStep
from attune.actions.sync.steps.set_system_settings import SetSystemSettingsStep
from attune.actions.sync.steps.sync_modules import SyncModulesStep
from attune.actions.sync.steps.sync_step import SyncStep


class SyncAction:
    def __init__(self):
        self.steps = []

    def register_step(self, step):
        if step is None:
            return
        if isinstance(step, SyncStep):
            self.steps.append(step)
        else:
            raise TypeError("Only SyncStep instances can be registered")

    def run(self):
        for step in self.steps:
            if step is None:
                continue
            print(f"\n{step.desc()}...")
            step.run()
        print("\nSync complete!")


def sync(reconfigure):
    action = SyncAction()
    action.register_step(GitPullStep.create())
    action.register_step(InstallGumStep.create())
    action.register_step(ConfigureAttuneStep.create(reconfigure))
    action.register_step(PatchDotfilesStep.create())
    action.register_step(SyncModulesStep.create())
    action.register_step(SetSystemSettingsStep.create())
    action.register_step(InstallFontsStep.create())
    action.register_step(FilterDockAppsStep.create())
    action.register_step(ApplyDefaultThemeStep.create())
    action.run()
