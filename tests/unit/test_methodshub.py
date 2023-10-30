import pytest

from ... import methodshub


class TestMethodsHubContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent(None, "lorem-ipsum.txt")

    def test_init_without_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("", "lorem-ipsum.txt")

    def test_init_with_empty_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", "")

    def test_init_with_invalid_url(self):
        with pytest.raises(ValueError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", "lorem-ipsum.txt")

    def test_init_with_github(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum", "lorem-ipsum.txt"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.txt"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"

    def test_init_with_github_git(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.txt"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.txt"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"

    def test_init_with_gitlab(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://gitlab.com/lorem/ipsum", "lorem-ipsum.txt"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.txt"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"

    def test_init_with_gitlab_git(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://gitlab.com/lorem/ipsum.git", "lorem-ipsum.txt"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.txt"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
