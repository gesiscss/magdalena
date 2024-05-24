# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import os.path
import re
import urllib.request
import uuid

import pytest

from ... import methodshub
from ...mybinder import MYBINDER_URL


class MockDocxResponse:
    def read():
        with open(
            os.path.join(os.path.dirname(__file__), "..", "assets", "minimal.docx"),
            "rb",
        ) as _file:
            docx = _file.read()

        return docx


class MockUui4:
    hex = "123-456-789"


def mock_uuid4():
    return MockUui4()


class TestMethodsHubHTTPContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent(None, filename="lorem-ipsum.docx")

    def test_init_without_filename(self, requests_mock):
        requests_mock.get(
            "http://lorem.ipsum/123",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        assert methodshub.MethodsHubHTTPContent("http://lorem.ipsum/123", filename=None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent("", filename="lorem-ipsum.md")

    def test_init_with_empty_filename(self, monkeypatch, requests_mock):
        requests_mock.get(
            "http://lorem.ipsum/123",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent(
                "http://lorem.ipsum/123", filename=""
            )

    def test_init_with_nextcloud(self, monkeypatch, requests_mock):
        requests_mock.get(
            "https://gesisbox.gesis.org/lorem/ipsum/download",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        methods_hub_content = methodshub.MethodsHubHTTPContent(
            "https://gesisbox.gesis.org/lorem/ipsum"
        )
        assert (
            methods_hub_content.source_url
            == "https://gesisbox.gesis.org/lorem/ipsum/download"
        )
        assert methods_hub_content.filename == "mock-file.docx"
        assert methods_hub_content.domain == "gesisbox.gesis.org"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gesisbox.gesis.org/123-456-789"
        )
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_nextcloud_complete(self, monkeypatch, requests_mock):
        requests_mock.get(
            "https://gesisbox.gesis.org/lorem/ipsum/download",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        methods_hub_content = methodshub.MethodsHubHTTPContent(
            "https://gesisbox.gesis.org/lorem/ipsum/download"
        )
        assert (
            methods_hub_content.source_url
            == "https://gesisbox.gesis.org/lorem/ipsum/download"
        )
        assert methods_hub_content.filename == "mock-file.docx"
        assert methods_hub_content.domain == "gesisbox.gesis.org"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gesisbox.gesis.org/123-456-789"
        )
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_sharepoint(self, monkeypatch, requests_mock):
        requests_mock.get(
            "https://gesisev.sharepoint.com/lorem/ipsum&download=1",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        methods_hub_content = methodshub.MethodsHubHTTPContent(
            "https://gesisev.sharepoint.com/lorem/ipsum"
        )
        assert (
            methods_hub_content.source_url
            == "https://gesisev.sharepoint.com/lorem/ipsum&download=1"
        )
        assert methods_hub_content.filename == "mock-file.docx"
        assert methods_hub_content.domain == "gesisev.sharepoint.com"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gesisev.sharepoint.com/123-456-789"
        )
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_sharepoint_complete(self, monkeypatch, requests_mock):
        requests_mock.get(
            "https://gesisev.sharepoint.com/lorem/ipsum&download=1",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        methods_hub_content = methodshub.MethodsHubHTTPContent(
            "https://gesisev.sharepoint.com/lorem/ipsum&download=1"
        )
        assert (
            methods_hub_content.source_url
            == "https://gesisev.sharepoint.com/lorem/ipsum&download=1"
        )
        assert methods_hub_content.filename == "mock-file.docx"
        assert methods_hub_content.domain == "gesisev.sharepoint.com"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gesisev.sharepoint.com/123-456-789"
        )
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_clone_or_pull(self, monkeypatch, requests_mock):
        requests_mock.get(
            "http://lorem.ipsum/123",
            body=MockDocxResponse(),
            headers={"Content-Disposition": 'filename="mock-file.docx"'},
        )

        with monkeypatch.context() as mock:
            mock.setattr(uuid, "uuid4", mock_uuid4)

            methods_hub_content = methodshub.MethodsHubHTTPContent(
                "http://lorem.ipsum/123"
            )
            methods_hub_content.clone_or_pull()

        assert os.path.isfile(
            os.path.join(methods_hub_content.tmp_path, methods_hub_content.filename)
        ), "Local copy of file not created."

    # def test_render_docx_to_html(self, monkeypatch):
    #     with monkeypatch.context() as mock:
    #         mock.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
    #         mock.setattr(uuid, "uuid4", mock_uuid4)

    #         methods_hub_content = methodshub.MethodsHubHTTPContent(
    #             "http://lorem.ipsum/123"
    #         )
    #         methods_hub_content.clone_or_pull()

    #     methods_hub_content.create_container()
    #     methods_hub_content._render_format("html")


class TestMethodsHubGitContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(None, filename="lorem-ipsum.md")

    def test_init_without_filename(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum", filename=None
        )
        assert methods_hub_content.source_url == "https://github.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "README.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("", filename="lorem-ipsum.md")

    def test_init_with_empty_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(
                "https://github.com/lorem/ipsum", filename=""
            )

    def test_init_with_invalid_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(
                "http://lorem.ipsum", filename="lorem-ipsum.md"
            )

    def test_init_with_github(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum", filename="lorem-ipsum.md"
        )
        assert methods_hub_content.source_url == "https://github.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_github_git(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", filename="lorem-ipsum.md"
        )
        assert methods_hub_content.source_url == "https://github.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_gitlab(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://gitlab.com/lorem/ipsum", filename="lorem-ipsum.md"
        )
        assert methods_hub_content.source_url == "https://gitlab.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_gitlab_git(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://gitlab.com/lorem/ipsum.git", filename="lorem-ipsum.md"
        )
        assert methods_hub_content.source_url == "https://gitlab.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_filename_extension_txt(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(
                "https://github.com/lorem/ipsum.git", filename="lorem-ipsum.txt"
            )

    def test_init_filename_extension_md(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", filename="lorem-ipsum.md"
        )
        assert methods_hub_content.source_url == "https://github.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_filename_extension_qmd(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", filename="lorem-ipsum.qmd"
        )
        assert methods_hub_content.source_url == "https://github.com/lorem/ipsum.git"
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.qmd"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"), "github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename_extension == "qmd"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_render_qmd_to_html_without_quarto(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units.git",
            filename="index.qmd",
            git_commit_id="996dbe13501f6cf3f2811843bee68cc5295dd0ff",
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units.git"
        )
        assert (
            methods_hub_content.git_commit_id
            == "996dbe13501f6cf3f2811843bee68cc5295dd0ff"
        )
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units"
        )
        assert methods_hub_content.filename == "index.qmd"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "GESIS-Methods-Hub"
        assert methods_hub_content.repository_name == "minimal-example-qmd-rstats-units"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"),
            "github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units",
        )
        assert methods_hub_content.filename_extension == "qmd"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

        with pytest.raises(AssertionError):
            methods_hub_content.create_container()

    def test_render_qmd_to_html_with_quarto(self, requests_mock):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units.git",
            filename="index.qmd",
            git_commit_id="c4add962323f877758bd679bfc94b6d26400d14c",
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units.git"
        )
        assert (
            methods_hub_content.git_commit_id
            == "c4add962323f877758bd679bfc94b6d26400d14c"
        )
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units"
        )
        assert methods_hub_content.filename == "index.qmd"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "GESIS-Methods-Hub"
        assert methods_hub_content.repository_name == "minimal-example-qmd-rstats-units"
        assert methods_hub_content.tmp_path == os.path.join(
            os.getenv("MAGDALENA_TMP"),
            "github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units",
        )
        assert methods_hub_content.filename_extension == "qmd"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

        mybinder_build_matcher = re.compile(f"^{MYBINDER_URL}/build")
        expected_mybinder_build_response = """
data: {"phase": "built", "imageName": "gesiscss/binder-r2d-g5b5b759-gesis-2dmethods-2dhub-2dminimal-2dexample-2dqmd-2drstats-2dunits-06c93c:c4add962323f877758bd679bfc94b6d26400d14c", "message": "Found built image, launching...\\n"}
data: {"phase": "ready", "message": "server running at https://notebooks.gesis.org/binder/jupyter/user/gesis-methods-h-md-rstats-units-gejw8fu0/\\n", "image": "gesiscss/binder-r2d-g5b5b759-gesis-2dmethods-2dhub-2dminimal-2dexample-2dqmd-2drstats-2dunits-06c93c:c4add962323f877758bd679bfc94b6d26400d14c", "repo_url": "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units", "token": "qKcb4Ja4Q12TqaR7zb8Tog", "binder_ref_url": "https://github.com/GESIS-Methods-Hub/minimal-example-qmd-rstats-units/tree/c4add962323f877758bd679bfc94b6d26400d14c", "binder_launch_host": "https://mybinder.org/", "binder_request": "v2/gh/GESIS-Methods-Hub/minimal-example-qmd-rstats-units/c4add962323f877758bd679bfc94b6d26400d14c", "binder_persistent_request": "v2/gh/GESIS-Methods-Hub/minimal-example-qmd-rstats-units/c4add962323f877758bd679bfc94b6d26400d14c", "url": "https://notebooks.gesis.org/binder/jupyter/user/gesis-methods-h-md-rstats-units-gejw8fu0/"}
"""
        requests_mock.get(mybinder_build_matcher, text=expected_mybinder_build_response)

        mybinder_status_matcher = re.compile(f"^{MYBINDER_URL}/jupyter/user/.*/api$")
        requests_mock.get(mybinder_status_matcher, json={"version": "mock"})

        mybinder_shutdown_matcher = re.compile(
            f"^{MYBINDER_URL}/jupyter/user/.*/api/shutdown$"
        )
        requests_mock.post(mybinder_shutdown_matcher)

        methods_hub_content.create_container()
        methods_hub_content._render_format("html")
