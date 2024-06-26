import os
import time

from attune.actions.set_theme.steps.set_background import SetBackgroundStep
from attune.actions.set_theme.steps.set_display_mode import SetDisplayModeStep
from attune.actions.set_theme.steps.set_oh_my_posh_theme import SetOhMyPoshThemeStep
from attune.actions.set_theme.steps.set_terminal_font import SetTerminalFontStep
from attune.actions.set_theme.steps.set_terminal_theme import SetTerminalThemeStep
from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.actions.set_theme.steps.set_vscode_color_theme import (
    SetVSCodeColorThemeStep,
)
from attune.actions.set_theme.steps.set_vscode_font import SetVSCodeFontStep
from attune.themes import get_theme_names, list_themes, set_active_theme_name


class SetThemeAction:
    def __init__(self):
        self.steps = []

    def register_step(self, step):
        if step is None:
            return
        if isinstance(step, SetThemeStep):
            self.steps.append(step)
        else:
            raise TypeError("Only SetThemeStep instances can be registered")

    def run(self, theme_name):
        for step in self.steps:
            step.run(theme_name)
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        set_active_theme_name(theme_name)
        print(f"Set active theme to: {theme_name}\n")


def set_theme(theme_name):
    # Validate theme name and get config
    if theme_name not in get_theme_names():
        print(f"Invalid theme name: {theme_name}")
        list_themes()
        return

    action = SetThemeAction()
    action.register_step(SetBackgroundStep.create())
    action.register_step(SetDisplayModeStep.create())
    action.register_step(SetOhMyPoshThemeStep.create())
    action.register_step(SetVSCodeColorThemeStep.create())
    action.register_step(SetVSCodeFontStep.create())
    action.register_step(SetTerminalThemeStep.create())
    action.register_step(SetTerminalFontStep.create())
    action.run(theme_name)
