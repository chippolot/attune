from attune import git
from attune.actions.sync.steps.sync_step import SyncStep
from attune.paths import get_repo_file_path


class GitPullStep(SyncStep):
    @staticmethod
    def create():
        return GitPullStep()

    def desc(self):
        return "Syncing attune repo"

    def run(self):
        git.pull(get_repo_file_path())
