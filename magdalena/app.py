# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import shutil

from flask import Flask

from .blueprint import magdalena


app = Flask(__name__)


with app.app_context():
    if "MAGDALENA_SHARED_DIR" not in os.environ:
        app.logger.warning("MAGDALENA_SHARED_DIR is not defined! Using default.")
        os.environ["MAGDALENA_SHARED_DIR"] = "/tmp/magdalena-shared-volume"
    shared_root_dir = os.getenv("MAGDALENA_SHARED_DIR")
    app.logger.info("Shared directory is %s", shared_root_dir)

    # Need to copy files to be able to share
    # because of Docker outside of Docker
    for dir_name in ("docker-scripts", "pandoc-filters"):
        app.logger.info("Copying %s to %s", dir_name, shared_root_dir)
        shutil.copytree(
            os.path.join("magdalena", dir_name),
            os.path.join(shared_root_dir, dir_name),
            dirs_exist_ok=True,
        )

    if "MAGDALENA_URL_PREFIX" not in os.environ:
        app.logger.warning("MAGDALENA_URL_PREFIX is not defined! Using default.")
    url_prefix = os.getenv("MAGDALENA_URL_PREFIX", None)
    app.logger.info("URL prefix is %s", url_prefix)

    app.register_blueprint(magdalena, url_prefix=url_prefix)
