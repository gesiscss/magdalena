# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import base64
import hashlib
import logging
import os
import os.path
import re
import subprocess
import urllib.request
import uuid
from zipfile import ZipFile

from lxml import etree
from lxml.cssselect import CSSSelector

import docker
import repo2docker

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from . import mybinder

logger = logging.getLogger("magdalena.app")

if "MAGDALENA_GRAPHQL_TARGET_URL" not in os.environ:
    logger.warning("MAGDALENA_GRAPHQL_TARGET_URL is not defined! Using localhost.")
    os.environ["MAGDALENA_GRAPHQL_TARGET_URL"] = "https://localhost"

GRAPHQL_TRANSPORT = RequestsHTTPTransport(
    url=os.getenv("MAGDALENA_GRAPHQL_TARGET_URL"),
    verify=True,
    retries=3,
    headers={"Authorization": f"Bearer {os.getenv('MAGDALENA_GRAPHQL_TARGET_TOKEN')}"},
)

GRAPHQL_CLIENT = Client(transport=GRAPHQL_TRANSPORT, fetch_schema_from_transport=True)


def extract_content_from_html(raw_html):
    """
    Extract content from html created by Quarto.
    """
    html = etree.fromstring(raw_html, etree.HTMLParser())
    selector = CSSSelector("main")
    selection = selector(html)

    if len(selection) > 0:
        logger.info("<main> was not found. Using <body> instead.")
        selector = CSSSelector("body")
        selection = selector(html)

    assert (
        len(selection) > 0
    ), "Selection from HTML document is empty. HTML document does NOT have <main> or <body>!"

    selection = selection[0]
    selection.tag = "div"

    return etree.tostring(selection, with_tail=False)


class MethodsHubContent:
    RENDER_MATRIX = {
        "md": {
            "html": "md2html.sh",
            "ipynb": "md2ipynb.sh",
        },
        "qmd": {
            "html": "qmd2html.sh",
            "ipynb": "qmd2ipynb.sh",
        },
        "Rmd": {
            "html": "Rmd2html.sh",
            "ipynb": "Rmd2ipynb.sh",
        },
        "ipynb": {
            "html": "ipynb2html.sh",
            "ipynb": "ipynb2ipynb.sh",
        },
        "docx": {
            "html": "docx2html.sh",
        },
    }

    def __init__(self, source_url, id_for_graphql=None):
        assert source_url is not None, "Source URL can NOT be None"
        assert len(source_url), "Source URL can NOT be empty string"
        self.source_url = source_url

        self.id_for_graphql = id_for_graphql

        self.http_to_git_repository = None
        self.user_name = None

        self.docker_repository = None
        self.docker_image_name = None
        self.docker_user_name = "magdalena"
        self.docker_user_id = os.getuid()  # This MUST be the host_user_id

        self.environment_for_container = {}

        self.docker_shared_dir = os.getenv("MAGDALENA_SHARED_DIR")
        assert self.docker_shared_dir is not None

        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.home_dir_at_docker = "/home/magdalena"
        self.render_at_dir = None

    def clone_or_pull(self):
        raise NotImplementedError

    def _start_repo2docker(self, repo):
        # Create container
        r2d = repo2docker.Repo2Docker()
        r2d.log_level = logging.DEBUG
        r2d.run = False
        r2d.push = False
        r2d.user_name = self.docker_user_name
        r2d.user_id = self.docker_user_id
        r2d.base_image = "gesiscss/repo2docker_base_image_with_quarto:v1.4.330"
        r2d.repo = repo
        r2d.output_image_spec = self.docker_image_name
        try:
            logger.info("Repository: %s", r2d.repo)
            logger.info("Docker image name: %s", r2d.output_image_spec)
            r2d.start()
        except Exception as err:
            logger.error(err)
            return False

    def create_container(self):
        raise NotImplementedError

    def _render_format(self, target_format):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"
        assert (
            target_format in self.RENDER_MATRIX[self.filename_extension]
        ), "Target format not supported!"

        script = self.RENDER_MATRIX[self.filename_extension][target_format]
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

        assert os.path.isfile(os.path.join(docker_scripts_location, script)), (
            "Script %s not found! Skipping execution." % script
        )

        host_user_id = os.getuid()
        host_group_id = os.getgid()

        volumes = {
            docker_scripts_location: {
                "bind": os.path.join(self.home_dir_at_docker, "_docker-scripts"),
                "mode": "ro",
            },
            pandoc_filters_location: {
                "bind": os.path.join(self.home_dir_at_docker, "_pandoc-filters"),
                "mode": "ro",
            },
            self.output_location: {"bind": output_location_in_container, "mode": "rw"},
        }
        logger.info(
            "Volumes in the sibling container: %s",
            volumes,
        )

        self.environment_for_container["output_location"] = output_location_in_container
        self.environment_for_container["docker_script_root"] = (
            f"{self.home_dir_at_docker}/_docker-scripts"
        )
        logger.info(
            "Environment variables in the sibling container: %s",
            self.environment_for_container,
        )

        logger.info("Running %s ...", script)
        client = docker.from_env()
        container = client.containers.run(
            self.docker_image_name,
            command=f"{self.home_dir_at_docker}/_docker-scripts/{script}",
            user=host_user_id,
            volumes=volumes,
            environment=self.environment_for_container,
            detach=True,
        )
        result = container.wait()
        logger.info(container.logs().decode("utf-8"))
        container.remove()

        assert result["StatusCode"] == 0, "Fail to render content"

    def _render_all_formats(self):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        for targe_format in self.RENDER_MATRIX[self.filename_extension]:
            self._render_format(targe_format)

    def render_formats(self, formats):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        for targe_format in formats:
            self._render_format(targe_format)

    def rendered_file(self, format):
        filename = f"index.{format}"
        return os.path.join(self.output_location, filename)

    def zip_all_formats(self):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        with ZipFile(self.zip_file_path, "w") as zip_with_all_formats:
            for targe_format in self.RENDER_MATRIX[self.filename_extension]:
                filename2zip = f"index.{targe_format}"
                zip_with_all_formats.write(
                    os.path.join(self.output_location, filename2zip),
                    arcname=filename2zip,
                )

    def zip_formats(self, formats):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        with ZipFile(self.zip_file_path, "w") as zip_output:
            for targe_format in formats:
                filename2zip = f"index.{targe_format}"
                zip_output.write(
                    os.path.join(self.output_location, filename2zip),
                    arcname=filename2zip,
                )

    def _push_rendered_format(self, target_format):
        mutation = gql(
            """
            mutation Mutation($input: CreateFileInput!) {
                createFile(input: $input) {
                    id
                }
            }
        """
        )

        filename2push = f"index.{target_format}"

        with open(filename2push, "rb") as _file:
            file_as_binary = b"".join(_file.readlines())

        if target_format != "html":
            file_base64 = base64.b64encode(file_as_binary)
        else:
            file_base64 = base64.b64encode(extract_content_from_html(file_as_binary))

        variables = {
            input: {
                "binary": file_base64,
                "fileExtension": target_format,
                "name": filename2push,
                "content": {"id": self.id_for_graphql},
            }
        }

        result = GRAPHQL_CLIENT.execute(mutation, variable_values=variables)
        logger.info("GraphQL call resulted in %s", result)

    def push_all_rendered_formats(self):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        for target_format in self.RENDER_MATRIX[self.filename_extension]:
            self._push_rendered_format(target_format)

    def push_rendered_formats(self, formats):
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File extension not supported!"

        for target_format in formats:
            self._push_rendered_format(target_format)


class MethodsHubHTTPContent(MethodsHubContent):
    def __init__(self, source_url, id_for_graphql=None, filename=None):
        MethodsHubContent.__init__(self, source_url, id_for_graphql)

        regex_match_http = re.match("https?://(.+?)/(.+)", self.source_url)

        assert regex_match_http is not None, "Source URL is invalid!"
        self.domain = regex_match_http.group(1)

        if self.domain == "gesisev.sharepoint.com" or "sharepoint" in self.domain:
            self.source_url = (
                self.source_url
                if self.source_url.endswith("&download=1")
                else f"{self.source_url}&download=1"
            )

        if (
            self.domain == "gesisbox.gesis.org"
            or "nextcloud" in self.domain
            or "ownCloud" in self.domain
        ):
            self.source_url = (
                self.source_url
                if self.source_url.endswith("/download")
                else f"{self.source_url}/download"
            )

        if filename is None:
            request = urllib.request.urlopen(self.source_url)
            assert request.status == 200, "Fail to stablish connection"
            regex_match_filename = re.search(
                r'filename="(.+)"', request.info()["Content-Disposition"]
            )
            assert (
                regex_match_filename is not None
            ), "Unable to extract filename from HTTP request"
            filename = regex_match_filename.group(1)
        assert len(filename), "filename can NOT be empty"

        self.filename = filename
        self.environment_for_container["file2render"] = self.filename

        self.tmp_path = os.path.join(
            os.getenv("MAGDALENA_TMP", "/tmp"), self.domain, uuid.uuid4().hex
        )

        self.filename_extension = self.filename.split(".")[-1]
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File format not supported!"

        self.output_location = f"{self.docker_shared_dir}/{self.domain}/{self.filename}"
        os.makedirs(self.output_location, exist_ok=True)

        self.zip_file_path = (
            f"{self.docker_shared_dir}/{self.domain}-{self.filename}.zip"
        )

    def clone_or_pull(self):
        os.makedirs(self.tmp_path, exist_ok=True)

        request = urllib.request.urlopen(self.source_url)
        assert request.status == 200, "Fail to stablish connection"
        with open(os.path.join(self.tmp_path, self.filename), "wb") as _file:
            _file.write(request.read())

    def create_container(self):
        self.docker_repository = f"magdalena/{self.domain}/{self.filename}"
        self.docker_repository = self.docker_repository.lower().replace(" ", "")

        with open(os.path.join(self.tmp_path, self.filename), "rb") as _file:
            hash = hashlib.md5(_file.read())

        self.docker_image_name = f"{self.docker_repository}:{hash.hexdigest()}"
        logger.info("Defined Docker image name: %s", self.docker_image_name)

        # Check if container already exists
        docker_client = docker.from_env()
        for docker_image in docker_client.images.list():
            for docker_image_tag in docker_image.tags:
                if docker_image_tag == self.docker_image_name:
                    logger.info("Docker image found. Skipping build.")
                    return

        self._start_repo2docker(self.tmp_path)


class MethodsHubGitContent(MethodsHubContent):
    def __init__(
        self, source_url, id_for_graphql=None, git_commit_id=None, filename=None
    ):
        MethodsHubContent.__init__(self, source_url, id_for_graphql)

        if filename is None:
            logger.warning("Filename is None. Using README.md.")
            filename = "README.md"

        assert len(filename), "filename can NOT be empty"

        if not source_url.endswith(".git"):
            logger.info("Git repository URL does NOT ends with '.git'")
            source_url = f"{source_url}.git"

        self.source_url = source_url
        self.git_commit_id = git_commit_id
        self.http_to_git_repository = self.source_url.replace(".git", "")
        self.filename = filename

        regex_match = re.match("https?://(.+?)/(.+?)/(.+?).git", self.source_url)

        assert regex_match is not None, "Git repository URL is invalid!"
        self.domain = regex_match.group(1)
        self.user_name = regex_match.group(2)
        self.repository_name = regex_match.group(3)

        self.tmp_path = os.path.join(
            os.getenv("MAGDALENA_TMP", "/tmp"),
            self.domain,
            self.user_name,
            self.repository_name,
        )

        self.filename_extension = self.filename.split(".")[-1]
        assert (
            self.filename_extension in self.RENDER_MATRIX
        ), "File format not supported!"

        self.output_location = f"{self.docker_shared_dir}/{self.domain}/{self.user_name}/{self.repository_name}/{self.filename}"
        os.makedirs(self.output_location, exist_ok=True)

        self.zip_file_path = f"{self.docker_shared_dir}/{self.domain}-{self.user_name}-{self.repository_name}-{self.filename}.zip"

        self.environment_for_container["github_https"] = self.http_to_git_repository
        self.environment_for_container["github_user_name"] = self.user_name
        self.environment_for_container["github_repository_name"] = self.repository_name
        self.environment_for_container["file2render"] = self.filename

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

        if self.git_commit_id is None:
            logger.warning("Git Commit ID is None. Using most recent commit.")
            git_get_id_subprocess = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=self.tmp_path, capture_output=True
            )
            assert (
                git_get_id_subprocess.returncode == 0
            ), "Fail to retrieve Git commit ID"
            self.git_commit_id = git_get_id_subprocess.stdout.decode().strip()

        git_commit_exists = subprocess.run(
            ["git", "show", self.git_commit_id, "--"],
            cwd=self.tmp_path,
            capture_output=True,
        )
        assert git_commit_exists.returncode == 0, (
            "Git commit with ID %s does NOT exists" % self.git_commit_id
        )
        logger.info("Git Commit ID: : %s", self.git_commit_id)

    def create_container(self):
        if self.git_commit_id is None:
            self.clone_or_pull()
            assert (
                self.git_commit_id is not None
            ), "Can NOT create Docker container if Git commit ID is None"

        if self.domain == "github.com":
            self.docker_image_name = mybinder.create_container_from_github(
                self.user_name, self.repository_name, self.git_commit_id
            )
        if self.domain == "gitlab.com":
            self.docker_image_name = mybinder.create_container_from_gitlab(
                self.user_name, self.repository_name, self.git_commit_id
            )

        assert self.docker_image_name is None, "Docker Image can NOT be None"
        self.docker_repository = self.docker_image_name.split(":")[0]
        self.environment_for_container["docker_image_name"] = self.docker_image_name
        logger.info("Defined Docker image name: %s", self.docker_image_name)

        # Check if container image already exists
        docker_client = docker.from_env()
        for docker_image in docker_client.images.list():
            for docker_image_tag in docker_image.tags:
                if docker_image_tag == self.docker_image_name:
                    logger.info("Docker image found. Skipping build.")
                    return

        # Donwload container image
        logger.info(
            "Docker image NOT found. Downloading image %s.", self.docker_image_name
        )
        docker_client.images.pull(self.docker_repository, self.git_commit_id)

        # Test if container has Quarto
        client = docker.from_env()
        container = client.containers.run(
            self.docker_image_name,
            command=f"which quarto",
            detach=True,
        )
        result = container.wait()
        logger.info(container.logs().decode("utf-8"))
        container.remove()

        assert result["StatusCode"] == 0, "Container does NOT have Quarto installed"
