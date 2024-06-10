import os

from attune.actions.set_theme.steps.set_theme_step import SetThemeStep
from attune.paths import get_repo_file_path
from attune.prompt import set_prompt_theme
from attune.themes import get_theme_param


class SetOhMyPoshThemeStep(SetThemeStep):
    @staticmethod
    def create():
        return SetOhMyPoshThemeStep()

    def run(self, theme_name):
        prompt_file = get_theme_param(theme_name, "prompt")
        if prompt_file is not None:
            print(f"Seting oh-my-posh prompt theme to: '{prompt_file}'")
            prompt_path = os.path.abspath(
                get_repo_file_path(f"themes/prompts/{prompt_file}", validate=True)
            )
            set_prompt_theme(prompt_path)
