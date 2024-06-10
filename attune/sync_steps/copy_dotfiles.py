from attune.paths import get_attune_file_path, get_repo_file_path
from attune.sync_steps.sync_step import SyncStep
from attune.template import template_apply


class SyncStepCopyDotfiles(SyncStep):
    @staticmethod
    def create():
        return SyncStepCopyDotfiles()

    def desc(self):
        return "Copying dotfiles"

    def run(self):
        copy_template(
            get_repo_file_path("dotfiles/.shell_profile", validate=True),
            get_attune_file_path(".shell_profile"),
        )
        copy_template(
            get_repo_file_path("dotfiles/.aliases", validate=True),
            get_attune_file_path(".aliases"),
        )
        copy_template(
            get_repo_file_path("dotfiles/.gitconfig", validate=True),
            get_attune_file_path(".gitconfig"),
        )


def copy_template(src, dst):
    with open(src, "r", encoding="utf-8") as file:
        src_content = file.read()
    src_content = template_apply(src_content)
    with open(dst, "w", encoding="utf-8") as file:
        file.write(src_content)

    print(f"'{dst}' copied.")
