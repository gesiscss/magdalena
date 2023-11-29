import logging
import os
import os.path
import re
import subprocess
import urllib.request
import uuid
from zipfile import ZipFile

import docker
import repo2docker

logger = logging.getLogger("magdalena.app")

class MethodsHubContent:
    RENDER_MATRIX = {
        "md": {
            "html": "md2html.sh",
            "qmd": "md2qmd.sh",
            "ipynb": "md2ipynb.sh",
        },
        "qmd": {
            "html": "qmd2html.sh",
            "qmd": "qmd2qmd.sh",
            "ipynb": "qmd2ipynb.sh",
        },
        "Rmd": {
            "html": "Rmd2html.sh",
            "qmd": "Rmd2qmd.sh",
            "ipynb": "Rmd2ipynb.sh",
        },
        "ipynb": {
            "html": "ipynb2html.sh",
            "qmd": "ipynb2qmd.sh",
            "ipynb": "ipynb2ipynb.sh",
        },
        "docx": {
            "md": "docx2md.sh",
            "html": "docx2html.sh",
        },
    }
    
    def __init__(self, source_url):
        assert source_url is not None, "Source URL can NOT be None"
        assert len(source_url) != 0, "Source URL can NOT be empty string"
        self.source_url = source_url

        self.docker_repository = None
        self.docker_image_name = None
        self.docker_user_name = "magdalena"
        self.docker_user_id = 1000  # This is the first user in Ubuntu

        self.docker_shared_dir = os.getenv("MAGDALENA_SHARED_DIR")
        assert self.docker_shared_dir is not None

        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.home_dir_at_docker = "/home/magdalena"
        self.render_at_dir = None

    def clone_or_pull(self):
        raise NotImplementedError
    
    def create_container(self):
        raise NotImplementedError
    
    def render_format(self, target_format):
        raise NotImplementedError
    
    def render_all_formats(self):
        raise NotImplementedError
    
    def zip_all_formats(self):
        raise NotImplementedError


class MethodsHubHTTPContent(MethodsHubContent):
    def __init__(self, source_url, filename=None):
        MethodsHubContent.__init__(self, source_url)

        regex_match_http = re.match("https?://(.+?)/(.+)", self.source_url)

        assert regex_match_http is not None, "Source URL is invalid!"
        self.domain = regex_match_http.group(1)

        if (
            self.domain == 'gesisev.sharepoint.com' or
            'sharepoint' in self.domain
        ):
            self.source_url = self.source_url if self.source_url.endswith("&download=1") else f"{self.source_url}&download=1"
        
        if (
            self.domain == 'gesisbox.gesis.org' or
            'nextcloud' in self.domain or
            'ownCloud' in self.domain
        ):
            self.source_url = self.source_url if self.source_url.endswith("/download") else f"{self.source_url}/download"

        if filename is None:
            request = urllib.request.urlopen(self.source_url)
            assert request.status == 200, "Fail to stablish connection"
            regex_match_filename = re.search(r'filename="(.+)"', request.info()['Content-Disposition'])
            assert regex_match_filename is not None, "Unable to extract filename from HTTP request" 
            filename = regex_match_filename.group(1)
        assert len(filename) != 0, "filename can NOT be empty"

        self.filename = filename
        
        self.tmp_path = f"_{self.domain}/{uuid.uuid4()}"

        self.filename_extension = self.filename.split(".")[-1]
        assert self.filename_extension in self.RENDER_MATRIX, "File format not supported!"

        self.output_location = f"{self.docker_shared_dir}/{self.domain}/{self.filename}"
        os.makedirs(self.output_location, exist_ok=True)

        self.zip_file_path = f"{self.docker_shared_dir}/{self.domain}-{self.filename}.zip"

    def clone_or_pull(self):
        request = urllib.request.urlopen(self.source_url)
        assert request.status == 200, "Fail to stablish connection"
        with open(self.filename, "wb") as _file:
            _file.write(request.read())

class MethodsHubGitContent(MethodsHubContent):
    def __init__(self, source_url, filename):
        MethodsHubContent.__init__(self, source_url)

        assert filename is not None, "filename can NOT be None"
        assert len(filename) != 0, "filename can NOT be empty"

        if not source_url.endswith(".git"):
            logger.info("Git repository URL does NOT ends with '.git'")
            source_url = f"{source_url}.git"

        self.source_url = source_url
        self.git_commit_id = None
        self.http_to_git_repository = self.source_url.replace(".git", "")
        self.filename = filename

        regex_match = re.match("https?://(.+?)/(.+?)/(.+?).git", self.source_url)

        assert regex_match is not None, "Git repository URL is invalid!"
        self.domain = regex_match.group(1)
        self.user_name = regex_match.group(2)
        self.repository_name = regex_match.group(3)

        self.tmp_path = f"_{self.domain}/{self.user_name}/{self.repository_name}"

        self.filename_extension = self.filename.split(".")[-1]
        assert self.filename_extension in self.RENDER_MATRIX, "File format not supported!"

        self.output_location = f"{self.docker_shared_dir}/{self.domain}/{self.user_name}/{self.repository_name}/{self.filename}"
        os.makedirs(self.output_location, exist_ok=True)

        self.zip_file_path = f"{self.docker_shared_dir}/{self.domain}-{self.user_name}-{self.repository_name}-{self.filename}.zip"

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
                ["git", "clone", self.source_url, self.tmp_path]
            )
            assert git_clone_subprocess.returncode == 0, "Fail to clone Git repository"

        git_get_id_subprocess = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.tmp_path, capture_output=True
        )
        assert git_get_id_subprocess.returncode == 0, "Fail to retrieve Git commit ID"
        self.git_commit_id = git_get_id_subprocess.stdout.decode().strip()

    def create_container(self):
        self.docker_repository = (
            f"magdalena/{self.domain}/{self.user_name}/{self.repository_name}"
        )
        self.docker_repository = self.docker_repository.lower()

        if self.git_commit_id is None:
            self.clone_or_pull()
            assert (
                self.git_commit_id is not None
            ), "Can NOT create Docker container if Git commit ID is None"

        self.docker_image_name = f"{self.docker_repository}:{self.git_commit_id}"
        logger.info("Defined Docker image name: %s", self.docker_image_name)

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
        r2d.user_name = self.docker_user_name
        r2d.user_id = self.docker_user_id
        r2d.base_image = "gesiscss/repo2docker_base_image_with_quarto:v1.4.330"
        r2d.repo = self.source_url
        # assert self.docker_image_name == 'magdalena/github.com/GESIS-Methods-Hub/minimal-example-ipynb-python:93a3b377f042298a65811a17356e25f30b276456'
        r2d.output_image_spec = self.docker_image_name
        try:
            logger.info("Repository: %s", r2d.repo)
            logger.info("Docker image name: %s", r2d.output_image_spec)
            r2d.start()
        except Exception as err:
            logger.error(err)
            return False

    def render_all_formats(self):
        if self.filename_extension not in self.RENDER_MATRIX:
            raise ValueError("File extension not supported!")

        docker_scripts_location = os.path.join(self.docker_shared_dir, "docker-scripts")
        pandoc_filters_location = os.path.join(self.docker_shared_dir, "pandoc-filters")
        output_location_in_container = self.docker_shared_dir

        logger.info("Location of docker_scripts directory: %s", docker_scripts_location)
        logger.info("Location of pandoc_filters directory: %s", pandoc_filters_location)
        logger.info("Location of output directory: %s", self.output_location)
        logger.info(
            "Location of output directory in the sibling container: %s",
            output_location_in_container,
        )

        host_user_id = os.getuid()
        host_group_id = os.getgid()
        mount_input_file = ""

        for script in self.RENDER_MATRIX[self.filename_extension]:
            if not os.path.isfile(os.path.join(docker_scripts_location, script)):
                logger.error("Script %s not found! Skipping execution.", script)
                continue

            logger.info("Running %s ...", script)
            render_content_subprocess = subprocess.run(
                f"""docker run \\
--user={host_user_id}:{host_group_id} \\
{mount_input_file} \\
--mount type=bind,source={docker_scripts_location},target={self.home_dir_at_docker}/_docker-scripts \\
--env docker_script_root={self.home_dir_at_docker}/_docker-scripts \\
--mount type=bind,source={pandoc_filters_location},target={self.home_dir_at_docker}/_pandoc-filters \\
--mount type=bind,source={self.output_location},target={output_location_in_container} \\
--env github_https={self.http_to_git_repository} \\
--env github_user_name={self.user_name} \\
--env github_repository_name={self.repository_name} \\
--env file2render={self.filename} \\
--env docker_image={self.docker_image_name} \\
--env output_location={output_location_in_container} \\
{self.docker_image_name} \\
/bin/bash -c '{self.home_dir_at_docker}/_docker-scripts/{script}'""",
                capture_output=True,
                shell=True,
            )

            assert render_content_subprocess.returncode == 0, "Fail to render content"

    def zip_all_formats(self):
        with ZipFile(self.zip_file_path, "w") as zip_with_all_formats:
            # FIXME The 'index' directory is being created in the Shell script
            zip_with_all_formats.write(
                os.path.join(self.output_location, "index", "index.html"),
                arcname="index.html",
            )
