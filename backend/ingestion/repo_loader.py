import os
import shutil
import subprocess
import time
from urllib.parse import urlparse


class RepoLoader:

    def __init__(
        self,
        base_path=r"C:\RepoMindData\repos"
    ):

        self.base_path = os.path.normpath(
            base_path
        )

        os.makedirs(
            self.base_path,
            exist_ok=True
        )

    # ============================================================
    # CHECK GITHUB URL
    # ============================================================

    def is_github_url(
        self,
        value
    ):

        if not value:
            return False

        value = value.strip()

        return value.startswith(
            (
                "https://github.com/",
                "http://github.com/",
                "https://www.github.com/",
                "http://www.github.com/"
            )
        )

    # ============================================================
    # GET REPOSITORY NAME
    # ============================================================

    def get_repository_name(
        self,
        repository_url
    ):

        parsed = urlparse(
            repository_url
        )

        path = parsed.path.strip(
            "/"
        )

        if path.endswith(".git"):

            path = path[:-4]

        repository_name = os.path.basename(
            path
        )

        if not repository_name:

            raise ValueError(
                "Could not determine repository name "
                "from the GitHub URL."
            )

        return repository_name

    # ============================================================
    # CHECK LOCAL REPOSITORY
    # ============================================================

    def is_local_repository(
        self,
        path
    ):

        if not path:
            return False

        path = os.path.normpath(
            path.strip()
        )

        if not os.path.isdir(
            path
        ):
            return False

        # A valid cloned repository normally
        # contains a .git directory.

        git_folder = os.path.join(
            path,
            ".git"
        )

        return os.path.isdir(
            git_folder
        )

    # ============================================================
    # REMOVE DIRECTORY SAFELY
    # ============================================================

    def _remove_existing_repository(
        self,
        repository_path
    ):

        if not os.path.exists(
            repository_path
        ):

            return True

        try:

            shutil.rmtree(
                repository_path
            )

            return True

        except (
            PermissionError,
            OSError
        ):

            return False

    # ============================================================
    # FIND SAFE CLONE DIRECTORY
    # ============================================================

    def _get_safe_repository_path(
        self,
        repository_name
    ):

        normal_path = os.path.join(
            self.base_path,
            repository_name
        )

        # --------------------------------------------------------
        # Directory doesn't exist
        # --------------------------------------------------------

        if not os.path.exists(
            normal_path
        ):

            return normal_path

        # --------------------------------------------------------
        # Try deleting it
        # --------------------------------------------------------

        if self._remove_existing_repository(
            normal_path
        ):

            return normal_path

        # --------------------------------------------------------
        # Folder is locked.
        # DO NOT FAIL.
        #
        # Create a new clone directory.
        # --------------------------------------------------------

        timestamp = time.strftime(
            "%Y%m%d_%H%M%S"
        )

        alternative_path = os.path.join(
            self.base_path,
            f"{repository_name}_{timestamp}"
        )

        counter = 1

        while os.path.exists(
            alternative_path
        ):

            alternative_path = os.path.join(
                self.base_path,
                f"{repository_name}_{timestamp}_{counter}"
            )

            counter += 1

        return alternative_path

    # ============================================================
    # LOAD REPOSITORY
    # ============================================================

    def clone_repository(
        self,
        repository_input
    ):

        if not repository_input:

            raise ValueError(
                "Repository URL cannot be empty."
            )

        repository_input = (
            repository_input
            .strip()
        )

        # ========================================================
        # CASE 1
        # Existing local repository
        # ========================================================

        if self.is_local_repository(
            repository_input
        ):

            repository_path = os.path.normpath(
                repository_input
            )

            print(
                "Using existing local repository:"
            )

            print(
                repository_path
            )

            return repository_path

        # ========================================================
        # CASE 2
        # GitHub repository
        # ========================================================

        if not self.is_github_url(
            repository_input
        ):

            raise ValueError(
                "Please provide a valid GitHub "
                "repository URL or an existing "
                "local repository path."
            )

        repository_name = (
            self.get_repository_name(
                repository_input
            )
        )

        repository_path = (
            self._get_safe_repository_path(
                repository_name
            )
        )

        print(
            f"Cloning repository:"
            f"\n{repository_input}"
        )

        print(
            f"Destination:"
            f"\n{repository_path}"
        )

        # ========================================================
        # GIT CLONE
        # ========================================================

        try:

            result = subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    repository_input,
                    repository_path
                ],

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="replace"
            )

        except FileNotFoundError:

            raise RuntimeError(
                "Git was not found on this system. "
                "Install Git and make sure 'git' "
                "is available in PATH."
            )

        # ========================================================
        # CHECK GIT RESULT
        # ========================================================

        if result.returncode != 0:

            # Try cleanup of partially cloned repo

            try:

                if os.path.exists(
                    repository_path
                ):

                    shutil.rmtree(
                        repository_path
                    )

            except Exception:

                pass

            error_message = (
                result.stderr
                or result.stdout
                or "Unknown Git error."
            )

            raise RuntimeError(
                "Git clone failed:\n"
                + error_message
            )

        # ========================================================
        # VERIFY CLONE
        # ========================================================

        if not os.path.isdir(
            repository_path
        ):

            raise RuntimeError(
                "Repository was cloned but the "
                "repository folder was not found."
            )

        print(
            "Repository cloned successfully."
        )

        return repository_path