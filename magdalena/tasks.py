# SPDX-FileCopyrightText: 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import shutil

from celery import shared_task
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger

from .methodshub import MethodsHubGitContent

logger = get_task_logger(__name__)

# Newly created files or directories created will have no privileges initially revoked
#
# We need this to avoid permission issues in the containers.
os.umask(0)


@celeryd_after_setup.connect
def setup_shared_dir(sender, instance, **kwargs):
    if "MAGDALENA_SHARED_DIR" not in os.environ:
        logger.warning("MAGDALENA_SHARED_DIR is not defined! Using default.")
        os.environ["MAGDALENA_SHARED_DIR"] = "/tmp/magdalena-shared-volume"
    shared_root_dir = os.getenv("MAGDALENA_SHARED_DIR")
    logger.info("Shared directory is %s", shared_root_dir)

    # Need to copy files to be able to share
    # because of Docker outside of Docker
    for dir_name in ("docker-scripts", "pandoc-filters"):
        logger.info("Copying %s to %s", dir_name, shared_root_dir)
        shutil.copytree(
            os.path.join("magdalena", dir_name),
            os.path.join(shared_root_dir, dir_name),
            dirs_exist_ok=True,
        )


@shared_task(bind=True, ignore_result=False)
def build(self, request_json):
    task = self

    task.update_state(state="VALIDATING")

    logger.info("Form content is %s", request_json)

    assert "source_url" in request_json, "Field source_url missing in form"

    assert "response" in request_json, "Field response missing in form"

    if "github.com" in request_json["source_url"]:
        source_url = request_json["source_url"]
    elif "gitlab.com" in request_json["source_url"]:
        source_url = request_json["source_url"]
    else:
        source_url = None
    assert source_url is None, "Source URL cannot be None"

    # assert "filename" in request_json, "Field filename missing in form"
    if "filename" not in request_json or len(request_json["filename"]) == 0:
        logger.warning("filename is not defined or empty! Using 'README.md'")
        filename = "README.md"
    else:
        filename = request_json["filename"]

    # assert "git_commit_id" in request_json, "Field git_commit_id missing in form"
    if "git_commit_id" not in request_json or len(request_json["git_commit_id"]) == 0:
        logger.warning("git_commit_id is not defined or empty!")
        git_commit_id = None
    else:
        git_commit_id = request_json["git_commit_id"]

    methods_hub_content = MethodsHubGitContent(
        source_url,
        git_commit_id=git_commit_id,
        filename=filename,
    )

    task.update_state(state="CLONING")
    methods_hub_content.clone_or_pull()

    task.update_state(state="DOCKERIZING")
    methods_hub_content.create_container()

    task.update_state(state="RENDERING")
    methods_hub_content.render_formats(request_json["target_format"])

    task.update_state(state="STORING")
    logger.info("Storing response for user")
    if len(request_json["target_format"]) == 1:
        return methods_hub_content.rendered_file(request_json["target_format"][0])
    else:
        assert methods_hub_content.zip_all_formats() is None, "Fail on zip formats"

        return methods_hub_content.zip_file_path
