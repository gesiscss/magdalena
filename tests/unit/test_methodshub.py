import urllib.request

import pytest

from ... import methodshub

class Mock200HTTPResponse:
    status = 200

    @staticmethod
    def info():
        return {
            'Content-Disposition': 'filename="mock-file.docx"'
        }

def mock_urlopen_with_200(url):
    return Mock200HTTPResponse()

class Mock404HTTPResponse:
    status = 404
    
class TestMethodsHubHTTPContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubHTTPContent(None, "lorem-ipsum.docx")

    def test_init_without_filename(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_with_200)

        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("http://lorem.ipsum", None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("", "lorem-ipsum.md")

    def test_init_with_empty_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("http://lorem.ipsum", "")



class TestMethodsHubGitContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(None, "lorem-ipsum.md")

    def test_init_without_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("http://lorem.ipsum", None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("", "lorem-ipsum.md")

    def test_init_with_empty_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("http://lorem.ipsum", "")

    def test_init_with_invalid_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent("http://lorem.ipsum", "lorem-ipsum.md")

    def test_init_with_github(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_github_git(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_gitlab(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://gitlab.com/lorem/ipsum", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.source_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_gitlab.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_with_gitlab_git(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://gitlab.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.source_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://gitlab.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_gitlab.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_filename_extension_txt(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubGitContent(
                "https://github.com/lorem/ipsum.git", "lorem-ipsum.txt"
            )

    def test_init_filename_extension_md(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None

    def test_init_filename_extension_qmd(self):
        methods_hub_content = methodshub.MethodsHubGitContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.qmd"
        )
        assert (
            methods_hub_content.source_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.git_commit_id is None
        assert (
            methods_hub_content.http_to_git_repository
            == "https://github.com/lorem/ipsum"
        )
        assert methods_hub_content.filename == "lorem-ipsum.qmd"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "qmd"
        assert methods_hub_content.docker_repository is None
        assert methods_hub_content.docker_image_name is None
