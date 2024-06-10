import platform

from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.paths import get_repo_file_path
from attune.terminal.terminal import get_terminal
from attune.themes import get_theme_param


class SetTerminalThemeStep(SetThemeStep):
    @staticmethod
    def create():
        if platform.system() == "Windows":
            return WindowsSetTerminalThemeStep()
        elif platform.system() == "Darwin":
            return MacSetTerminalThemeStep()
        else:
            raise Exception("Unsupported platform")

    def run(self, theme_name):
        pass


class WindowsSetTerminalThemeStep(SetTerminalThemeStep):
    def run(self, theme_name):
        terminal = get_terminal()

        # Set Terminal Color Scheme
        term_scheme_name = get_theme_param(theme_name, "terminal.color_scheme.name")
        if term_scheme_name is not None:
            print(f"Seting terminal color scheme to: {term_scheme_name}")
            term_scheme_file = get_theme_param(
                theme_name, "terminal.color_scheme.fileid"
            )
            term_scheme_path = None
            if term_scheme_file is not None:
                term_scheme_path = get_repo_file_path(
                    f"themes/terminal/windows/{term_scheme_file}.scheme.json",
                    validate=True,
                )
                terminal.set_color_scheme(term_scheme_name, term_scheme_path)

        # Set Terminal Theme
        term_theme_name = get_theme_param(theme_name, "terminal.theme.name")
        if term_theme_name is not None:
            print(f"Seting terminal theme to: {term_theme_name}")
            term_theme_file = get_theme_param(theme_name, "terminal.theme.fileid")
            term_theme_path = None
            if term_theme_file is not None:
                term_theme_path = get_repo_file_path(
                    f"themes/terminal/windows/{term_theme_file}.theme.json",
                    validate=True,
                )
                terminal.set_theme(term_theme_name, term_theme_path)

        # Set Other Terminal Params
        terminal.set_theme_setting("opacity", theme_name, "terminal.opacity")
        terminal.set_theme_setting("useAcrylic", theme_name, "terminal.useAcrylic")
        terminal.set_theme_setting("cursorShape", theme_name, "terminal.cursorShape")


class MacSetTerminalThemeStep(SetTerminalThemeStep):
    def run(self, theme_name):
        terminal = get_terminal()

        # Set terminal theme
        term_theme_name = get_theme_param(theme_name, "terminal.color_scheme.name")
        if term_theme_name is not None:
            print(f"Seting terminal theme to: {term_theme_name}")
            term_theme_file = get_theme_param(
                theme_name, "terminal.color_scheme.fileid"
            )
            term_theme_path = None
            if term_theme_file is not None:
                term_theme_path = get_repo_file_path(
                    f"themes/terminal/mac/{term_theme_file}.terminal", validate=True
                )
                terminal.set_theme(term_theme_name, term_theme_path)

        # TODO Support changing opacity
