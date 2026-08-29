import os
import shutil
from git import Repo


class RepositoryLoader:

    def __init__(self, repo_url: str, destination: str = "data/repository"):
        self.repo_url = repo_url
        self.destination = destination

    def clone_repository(self):

        # Remove old repository if it exists
        if os.path.exists(self.destination):
            shutil.rmtree(self.destination)

        print("Cloning repository...")
        print(f"URL: {self.repo_url}")

        Repo.clone_from(
            self.repo_url,
            self.destination
        )

        print("Repository cloned successfully!")

        return self.destination