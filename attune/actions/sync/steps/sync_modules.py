from attune import modules
from attune.actions.sync.steps.sync_step import SyncStep


class SyncModulesStep(SyncStep):
    @staticmethod
    def create():
        return SyncModulesStep()

    def desc(self):
        return "Syncing attune modules"

    def run(self):
        for module in modules.get_installed_modules():
            modules.sync(module.get("url"))
