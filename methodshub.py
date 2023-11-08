import logging
import os.path
import re
import subprocess

import docker
import repo2docker

logger = logging.getLogger("magdalena.app")


class MethodsHubContent:
    def __init__(self, git_repository_url, filename):
        assert git_repository_url is not None, "Git repository can NOT be None"
        assert filename is not None, "filename can NOT be None"

        assert len(git_repository_url) != 0, "Git repository can NOT be empty string"
        assert len(filename) != 0, "filename can NOT be empty string"

        if not git_repository_url.endswith(".git"):
            logger.info("Git repository URL does NOT ends with '.git'")
            git_repository_url = f"{git_repository_url}.git"

        self.git_repository_url = git_repository_url
        self.git_commit_id = None
        self.http_to_git_repository = self.git_repository_url.replace(".git", "")
        self.filename = filename

        regex_match = re.match("https?://(.*)/(.*)/(.*).git", self.git_repository_url)

        if regex_match:
            self.domain = regex_match.group(1)
            self.user_name = regex_match.group(2)
            self.repository_name = regex_match.group(3)
        else:
            raise ValueError("Git repository URL is invalid!")

        self.tmp_path = f"_{self.domain}/{self.user_name}/{self.repository_name}"

        self.filename_extension = self.filename.split(".")[-1]
        assert self.filename_extension in (
            "md",
            "qmd",
            "Rmd",
            "ipynb",
            "docx",
        ), "File format not supported!"

        self.docker_repository = None
        self.docker_image_name = None

    def clone_or_pull(self):
        if os.path.exists(self.tmp_path):
            logger.info("Running git pull")
            git_pull_subprocess = subprocess.run(
                ["git", "pull", "origin"], cwd=self.tmp_path
            )
            assert git_pull_subprocess.returncode == 0, "Fail to update Git repository"
        else:
            logger.info("Running git clone")
            git_clone_subprocess = subprocess.run(
                ["git", "clone", self.git_repository_url, self.tmp_path]
            )
            assert git_clone_subprocess.returncode == 0, "Fail to clone Git repository"

        git_get_id_subprocess = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.tmp_path, capture_output=True
        )
        assert git_get_id_subprocess.returncode == 0, "Fail to retrieve Git commit ID"
        self.git_commit_id = git_get_id_subprocess.stdout.decode().strip()

        return True

    def create_container(self):
        self.docker_repository = (
            f"magdalena/{self.domain}/{self.user_name}/{self.repository_name}"
        )

        if self.git_commit_id is None:
            self.clone_or_pull()
            assert (
                self.git_commit_id is not None
            ), "Can NOT create Docker container if Git commit ID is None"

        self.docker_image_name = f"{self.docker_repository}:{self.git_commit_id}"

        # Check if container already exists
        docker_client = docker.from_env()
        for docker_image in docker_client.images.list():
            for docker_image_tag in docker_image.tags:
                if docker_image_tag == self.docker_image_name:
                    logger.info("Docker image found. Skipping build.")
                    return True

        # Create container
        r2d = repo2docker.Repo2Docker()
        r2d.log_level = logging.DEBUG
        r2d.run = False
        r2d.push = False
        r2d.user_name = "magdalena"
        r2d.user_id = 1000  # This is the first user in Ubuntu
        r2d.base_image = "gesiscss/repo2docker_base_image_with_quarto:v1.4.330"
        r2d.repo = self.git_repository_url
        r2d.output_image_spec = self.docker_image_name
        try:
            logger.info("Repository: %s", r2d.repo)
            logger.info("Docker image name: %s", r2d.output_image_spec)
            r2d.start()
        except Exception as err:
            logger.error(err)
            return False

        return True

    def render_all_formats(self):
        RENDER_MATRIX = {
            "md": (
                "md2md.sh",
                "md2qmd.sh",
                "md2ipynb.sh"
            ),
            "qmd": (
                "qmd2md.sh",
                "qmd2qmd.sh",
                "qmd2ipynb.sh"
            ),
            "Rmd": (
                "Rmd2md.sh",
                "Rmd2qmd.sh",
                "Rmd2ipynb.sh"
            ),
            "ipynb": (
                "ipynb2md.sh",
                "ipynb2qmd.sh",
                "ipynb2ipynb.sh"
            ),
            "docx": (
                "docx2md.sh"
            )
        }

        if self.filename_extension not in RENDER_MATRIX:
            raise ValueError("File extension not supported!")

        return True
