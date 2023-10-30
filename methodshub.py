import logging

import re


class MethodsHubContent:
    def __init__(self, git_repository_url, filename):
        if not git_repository_url.endswith(".git"):
            logging.info("Git repository URL does NOT ends with '.git")
            git_repository_url = f"{git_repository_url}.git"

        self.git_repository_url = git_repository_url
        self.filename = filename

        regex_match = re.match("https?://(.*)/(.*)/(.*).git", self.git_repository_url)

        if regex_match:
            self.domain = regex_match.group(1)
            self.user_name = regex_match.group(2)
            self.repository_name = regex_match.group(3)
        else:
            raise ValueError("Git repository URL is invalid!")
