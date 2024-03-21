import os.path
import urllib.request
import uuid

import pytest

from ... import methodshub


class Mock200HTTPResponse:
    status = 200

    @staticmethod
    def info():
        return {"Content-Disposition": 'filename="mock-file.docx"'}

    @staticmethod
    def read():
        with open(
            os.path.join(os.path.dirname(__file__), "..", "assets", "minimal.docx"),
            "rb",
        ) as _file:
            docx = _file.read()

        return docx


def mock_urlopen_with_200(url):
    return Mock200HTTPResponse()


class Mock404HTTPResponse:
    status = 404


def mock_urlopen_with_404(url):
    return Mock404HTTPResponse()


class MockUui4:
    hex = "123-456-789"


def mock_uuid4():
    return MockUui4()


class TestMethodsHubHTTPContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent(None, filename="lorem-ipsum.docx")

    def test_init_without_filename(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)

        assert methodshub.MethodsHubHTTPContent("http://lorem.ipsum/123", filename=None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent("", filename="lorem-ipsum.md")

    def test_init_with_empty_filename(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
        monkeypatch.setattr(uuid, "uuid4", mock_uuid4)

        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent(
                "http://lorem.ipsum/123", filename=""
            )

    def test_init_with_nextcloud(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
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
        assert methods_hub_content.tmp_path == "/tmp/gesisbox.gesis.org/123-456-789"
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_nextcloud_complete(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
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
        assert methods_hub_content.tmp_path == "/tmp/gesisbox.gesis.org/123-456-789"
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_sharepoint(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
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
        assert methods_hub_content.tmp_path == "/tmp/gesisev.sharepoint.com/123-456-789"
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_sharepoint_complete(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
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
        assert methods_hub_content.tmp_path == "/tmp/gesisev.sharepoint.com/123-456-789"
        assert methods_hub_content.filename_extension == "docx"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_clone_or_pull(self, monkeypatch):
        with monkeypatch.context() as mock:
            mock.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
            mock.setattr(uuid, "uuid4", mock_uuid4)

            methods_hub_content = methodshub.MethodsHubHTTPContent(
                "http://lorem.ipsum/123"
            )
            methods_hub_content.clone_or_pull()

        assert os.path.isfile(
            os.path.join(methods_hub_content.tmp_path, methods_hub_content.filename)
        ), "Local copy of file not created."

    def test_render_format_docx_to_html(self, monkeypatch):
        with monkeypatch.context() as mock:
            mock.setattr(urllib.request, "urlopen", mock_urlopen_with_200)
            mock.setattr(uuid, "uuid4", mock_uuid4)

            methods_hub_content = methodshub.MethodsHubHTTPContent(
                "http://lorem.ipsum/123"
            )
            methods_hub_content.clone_or_pull()

        methods_hub_content.create_container()
        methods_hub_content._render_format("html")


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
        assert methods_hub_content.tmp_path == "/tmp/github.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/github.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/github.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/gitlab.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/gitlab.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/github.com/lorem/ipsum"
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
        assert methods_hub_content.tmp_path == "/tmp/github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "qmd"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None
