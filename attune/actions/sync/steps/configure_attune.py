from attune import gum, module
from attune.actions.sync.steps.sync_step import SyncStep
from attune.config import Config
from attune.module import Modules

ALWAYS_CONFIGURE = True


class ConfigureAttuneStep(SyncStep):
    @staticmethod
    def create():
        return ConfigureAttuneStep()

    def desc(self):
        return "Checking attune configuration"

    def run(self):
        if Config.exists() and not ALWAYS_CONFIGURE:
            print("Already configured!")
            return

        config = Config.load()

        gum.style(
            "Welcome to attue!\nLet's configure your experience!",
            foreground=212,
            border_foreground=212,
            border="double",
            align="center",
            width=50,
            margin="1 2",
            padding="2 4",
        )

        # Choose modules to enable
        modules_to_enable = gum.choose(
            choices=module.get_all(),
            header="Which modules do you want to enable?",
            limit=None,
        )
        module.clear()
        for m in modules_to_enable:
            module.enable(m)

        if module.is_enabled(Modules.GIT):
            config.set("git.name", gum.input(prompt="Enter your git name: "))
            config.set("git.email", gum.input(prompt="Enter your git email: "))
