import os
import shutil

from git import Repo


class RepoLoader:

    def __init__(self, base_path="data/repos"):

        self.base_path = base_path

        os.makedirs(
            self.base_path,
            exist_ok=True
        )

    def clone_repository(self, repo_url):

        repo_name = repo_url.rstrip("/").split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        repo_path = os.path.join(
            self.base_path,
            repo_name
        )

        # Remove existing repository
        # so we always work with a fresh copy
        if os.path.exists(repo_path):

            shutil.rmtree(
                repo_path
            )

        print(
            f"\nCloning repository: "
            f"{repo_url}"
        )

        Repo.clone_from(
            repo_url,
            repo_path
        )

        print(
            f"Repository cloned to: "
            f"{repo_path}"
        )

        return repo_path