"""
Wrap around mybinder.org / binderhub API.

Documentation at https://binderhub.readthedocs.io/en/latest/api.html.
"""

import datetime
import json
import logging
import os
import urllib.parse

import requests

MYBINDER_URL = os.getenv("MYBINDER_URL", "https://mybinder.org")
REQUESTS_TIMEOUT = 30  # seconds
USER_TIMEOUT = 300  # seconds or 5min

logger = logging.getLogger("magdalena.app")


def create_container_from_github(user, repo, commit_id="main"):
    provider_prefix = "gh"
    spec = f"{user}/{repo}/{commit_id}"
    return _create_container(provider_prefix, spec)


def create_container_from_gitlab(user, repo, commit_id="main"):
    project_id = urllib.parse.quote(f"{user}/{repo}", safe="")

    provider_prefix = "gl"
    spec = f"{project_id}/{commit_id}"
    return _create_container(provider_prefix, spec)


def _create_container(provider_prefix, spec):
    """
    We can launch an image that most likely already has been built.
    """
    build_url = f"{MYBINDER_URL}/build/{provider_prefix}/{spec}"

    notebook_url = None
    token = None
    container_name = None

    begin_of_request = datetime.datetime.now()

    response = requests.get(build_url, stream=True, timeout=REQUESTS_TIMEOUT)
    response.raise_for_status()
    for line in response.iter_lines():
        now = datetime.datetime.now()
        request_duration = now - begin_of_request
        if request_duration.seconds > USER_TIMEOUT:
            logger.error("Timeout")
            response.close()
            break

        line = line.decode("utf8")
        if line.startswith("data:"):
            data = json.loads(line.split(":", 1)[1])

            if data.get("message") is not None:
                logger.info(
                    "| %-15s | %s", data.get("phase"), data.get("message").strip()
                )
            else:
                logger.info("| %-15s | %s", "missing phase", line)

            if data.get("phase") == "built":
                container_name = data.get("imageName")

            if data.get("phase") == "ready":
                notebook_url = data["url"]
                token = data["token"]
                break
        else:
            logger.info(logger.info("| %-15s | %s", "missing data", line), line)
    else:
        assert False, "%s never returned a 'Ready'" % MYBINDER_URL

    assert container_name is not None, "Unknow container name"
    assert token is not None, "toke is None"

    headers = {"Authorization": f"token {token}"}
    response = requests.get(
        notebook_url + "/api", headers=headers, timeout=REQUESTS_TIMEOUT
    )
    assert response.status_code == 200
    assert "version" in response.json()
    logger.info("Jupyter single user server is running!")

    response = requests.post(
        notebook_url + "/api/shutdown", headers=headers, timeout=REQUESTS_TIMEOUT
    )
    assert response.status_code == 200
    logger.info("Jupyter single user server was shutdown!")

    return container_name
