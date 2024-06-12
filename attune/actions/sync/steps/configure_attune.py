from attune.actions.sync.steps.sync_step import SyncStep


class ConfigureAttuneStep(SyncStep):
    @staticmethod
    def create():
        return ConfigureAttuneStep()

    def desc(self):
        return "Checking attune configuration"

    def run(self):
        # TODO implement
        pass
