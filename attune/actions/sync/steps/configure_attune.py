import platform

from attune import gum, module
from attune.actions.sync.steps.sync_step import SyncStep
from attune.config import Config
from attune.module import Modules
from attune.themes import get_theme_names, set_active_theme_name, set_default_theme_name


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

        config = Config.load()
        if self.__module_check(Modules.GIT):
            config.set("git.name", gum.input(prompt="Enter your git name: "))
            config.set("git.email", gum.input(prompt="Enter your git email: "))

        self.__module_check(Modules.VSCODE)

        if platform.system() == "Darwin":
            self.__module_check(Modules.CHATGPT)

        config.set(
            "shell.default_dir",
            gum.input(prompt="Enter your home directory: ", placeholder="~/"),
        )
        config.save()

        # Let the user select a default theme
        default_theme_name = gum.choose(
            get_theme_names(), header="Select a default theme: "
        )
        if default_theme_name is not None:
            set_default_theme_name(default_theme_name)
            set_active_theme_name(None)

        print("Configuration complete! Enjoy attuning!")

    def __module_check(self, m):
        if gum.confirm(f"Do you want attune to manage {m} for you?"):
            module.enable(m)
            return True
        return False
