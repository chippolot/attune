from attune.dotfiles import replace_dotfile_line, DotfileSource


def set_prompt_theme(prompt_path):
    replace_dotfile_line(
        DotfileSource.ATTUNE,
        ".env",
        r"export OMP_THEME=.*",
        f'export OMP_THEME="{prompt_path}"',
    )
