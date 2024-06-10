import subprocess

from attune.paths import get_repo_file_path
from attune.sync_steps.sync_step import SyncStep


class SyncStepGitPull(SyncStep):
    @staticmethod
    def create():
        return SyncStepGitPull()

    def desc(self):
        return "Syncing attune repo"

    def run(self):
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd=get_repo_file_path(),
                check=True,
                text=True,
                capture_output=True,
            )
            print(result.stdout.strip("\n"))
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running git pull: {e.stderr}")
