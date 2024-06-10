from attune.sync_steps.apply_default_theme import SyncStepApplyDefaultTheme
from attune.sync_steps.copy_dotfiles import SyncStepCopyDotfiles
from attune.sync_steps.git_pull import SyncStepGitPull
from attune.sync_steps.install_apps import SyncStepInstallApps
from attune.sync_steps.install_fonts import SyncStepInstallFonts
from attune.sync_steps.patch_dotfiles import SyncStepPatchDotfiles
from attune.sync_steps.sync_step import SyncStep
from attune.sync_steps.set_system_settings import SyncStepSetSystemSettings


class SyncAction:
    def __init__(self):
        self.steps = []

    def register_step(self, step):
        if isinstance(step, SyncStep):
            self.steps.append(step)
        else:
            raise TypeError("Only SyncStep instances can be registered")

    def run(self):
        for step in self.steps:
            print(f"\n{step.desc()}...")
            step.run()
        print("\nSync complete!")


def sync(args=None):
    sync_action = SyncAction()
    sync_action.register_step(SyncStepGitPull.create())
    sync_action.register_step(SyncStepPatchDotfiles.create())
    sync_action.register_step(SyncStepCopyDotfiles.create())
    sync_action.register_step(SyncStepSetSystemSettings.create())
    sync_action.register_step(SyncStepInstallApps.create())
    sync_action.register_step(SyncStepInstallFonts.create())
    sync_action.register_step(SyncStepApplyDefaultTheme.create())
    sync_action.run()
