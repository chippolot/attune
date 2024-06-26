import os

from attune import template
from attune.actions.sync.steps.sync_step import SyncStep
from attune.config import Config
from attune.paths import get_repo_file_path
from attune.shell import get_profile_filename


class PatchDotfilesStep(SyncStep):
    @staticmethod
    def create():
        return PatchDotfilesStep()

    def desc(self):
        return "Patching dotfiles with setup code"

    def run(self):
        patch_setup_block(
            os.path.expanduser(f"~/{get_profile_filename()}"),
            get_repo_file_path("dotfiles/setup/.shell_profile", validate=True),
        )
        patch_setup_block(
            os.path.expanduser("~/.gitconfig"),
            get_repo_file_path("dotfiles/setup/.gitconfig", validate=True),
        )


def patch_setup_block(file_to_patch, setup_block_file):
    block_start_marker = "# >> Attune Setup Start >> DO NOT MODIFY"
    block_end_marker = "# >> Attune Setup End >> DO NOT MODIFY"

    # Load file to patch
    if os.path.exists(file_to_patch):
        with open(file_to_patch, "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = []

    # Load block
    with open(setup_block_file, "r", encoding="utf-8") as file:
        setup_block = file.read()

    # Apply template replacements
    setup_block = template.apply(setup_block, Config.load()._cfg)

    # Apply block markers
    setup_block = f"{block_start_marker}\n{setup_block}\n{block_end_marker}"

    # Split setup block into lines
    setup_block_lines = [line + "\n" for line in setup_block.split("\n")]

    # Find the start and end of the existing block, if any
    start_index = end_index = -1
    for i, line in enumerate(lines):
        if block_start_marker in line:
            start_index = i
        if block_end_marker in line:
            end_index = i
            break

    # Check if the existing block is the same as the new block
    if start_index != -1 and end_index != -1:
        existing_block_lines = lines[start_index : end_index + 1]
        if existing_block_lines == setup_block_lines:
            print(f"'{file_to_patch}' is already up-to-date.")
            return

    # Replace the existing block if found, otherwise append the new block
    if start_index != -1 and end_index != -1:
        lines[start_index : end_index + 1] = setup_block_lines
    else:
        lines.append("\n")
        lines.extend(setup_block_lines)

    # Rewrite patched file
    with open(file_to_patch, "w", encoding="utf-8") as file:
        file.writelines(lines)

    print(f"'{file_to_patch}' patched.")
