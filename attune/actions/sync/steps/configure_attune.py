from attune import gum, module
from attune.actions.sync.steps.sync_step import SyncStep
from attune.config import Config
from attune.module import Modules
from attune.themes import set_active_theme_name


class ConfigureAttuneStep(SyncStep):
    reconfigure = False

    @staticmethod
    def create(reconfigure):
        return ConfigureAttuneStep(reconfigure)

    def __init__(self, reconfigure) -> None:
        super().__init__()
        self.reconfigure = reconfigure

    def desc(self):
        return "Checking attune configuration"

    def forceRun(self):
        self.__runImpl()

    def run(self):
        if Config.exists() and not self.reconfigure:
            print("Already configured!")
            return
        self.__runImpl()

    def __runImpl(self):
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

        module.clear()

        # TODO Make config a singleton to prevent saving-over
        config = Config.load()
        if self.__module_check(Modules.GIT):
            config.set("git.name", gum.input(prompt="Enter your git name: "))
            config.set("git.email", gum.input(prompt="Enter your git email: "))

        self.__module_check(Modules.VSCODE)

        config.set(
            "shell.default_dir",
            gum.input(prompt="Enter your home directory: ", placeholder="~/"),
        )
        config.save()

        set_active_theme_name(None)

        print("Configuration complete! Enjoy attuning!")

    def __module_check(self, m):
        if gum.confirm(f"Do you want attune to manage {m} for you?"):
            module.enable(m)
            return True
        return False
