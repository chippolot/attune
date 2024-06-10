import subprocess

from attune.actions.sync.steps.sync_step import SyncStep
from attune.paths import get_repo_file_path


class GitPullStep(SyncStep):
    @staticmethod
    def create():
        return GitPullStep()

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
