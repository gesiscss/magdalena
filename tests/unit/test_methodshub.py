import pytest

from ... import methodshub


class TestMethodsHubContent:
    def test_init_without_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent(None, "lorem-ipsum.md")

    def test_init_without_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", None)

    def test_init_with_empty_url(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("", "lorem-ipsum.md")

    def test_init_with_empty_filename(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", "")

    def test_init_with_invalid_url(self):
        with pytest.raises(ValueError):
            assert methodshub.MethodsHubContent("http://lorem.ipsum", "lorem-ipsum.md")

    def test_init_with_github(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"

    def test_init_with_github_git(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"

    def test_init_with_gitlab(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://gitlab.com/lorem/ipsum", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_gitlab.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"

    def test_init_with_gitlab_git(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://gitlab.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://gitlab.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "gitlab.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_gitlab.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"

    def test_init_filename_extension_txt(self):
        with pytest.raises(AssertionError):
            assert methodshub.MethodsHubContent(
                "https://github.com/lorem/ipsum.git", "lorem-ipsum.txt"
            )

    def test_init_filename_extension_md(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.md"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.md"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "md"

    def test_init_filename_extension_qmd(self):
        methods_hub_content = methodshub.MethodsHubContent(
            "https://github.com/lorem/ipsum.git", "lorem-ipsum.qmd"
        )
        assert (
            methods_hub_content.git_repository_url
            == "https://github.com/lorem/ipsum.git"
        )
        assert methods_hub_content.filename == "lorem-ipsum.qmd"
        assert methods_hub_content.domain == "github.com"
        assert methods_hub_content.user_name == "lorem"
        assert methods_hub_content.repository_name == "ipsum"
        assert methods_hub_content.tmp_path == "_github.com/lorem/ipsum"
        assert methods_hub_content.filename_extension == "qmd"
