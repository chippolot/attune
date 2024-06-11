from attune.actions.sync.steps.sync_step import SyncStep
from attune.paths import get_attune_file_path, get_repo_file_path
from attune.shell import get_profile_filename
from attune.template import template_apply


class CopyDotfilesStep(SyncStep):
    @staticmethod
    def create():
        return CopyDotfilesStep()

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
        copy_template(
            get_repo_file_path(f"dotfiles/{get_profile_filename()}", validate=True),
            get_attune_file_path(get_profile_filename()),
        )


def copy_template(src, dst):
    with open(src, "r", encoding="utf-8") as file:
        src_content = file.read()
    src_content = template_apply(src_content)
    with open(dst, "w", encoding="utf-8") as file:
        file.write(src_content)

    print(f"'{dst}' copied.")
