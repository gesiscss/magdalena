import logging

import re


class MethodsHubContent:
    def __init__(self, git_repository_url, filename):
        assert git_repository_url is not None, "Git repository can NOT be None"
        assert filename is not None, "filename can NOT be None"

        assert len(git_repository_url) != 0, "Git repository can NOT be empty string"
        assert len(filename) != 0, "filename can NOT be empty string"

        if not git_repository_url.endswith(".git"):
            logging.info("Git repository URL does NOT ends with '.git")
            git_repository_url = f"{git_repository_url}.git"

        self.git_repository_url = git_repository_url
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
