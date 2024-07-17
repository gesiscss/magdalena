# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from celery import Celery
from celery import Task
from flask import Flask


def create_app():
    import logging
    import os
    import shutil

    from flask import Flask

    import jwt

    from .methodshub import MethodsHubHTTPContent, MethodsHubGitContent

    from .pem import (
        retrieve_public_key,
        KEYCLOAK_ISSUER,
    )

    from .views import bp

    # Newly created files or directories created will have no privileges initially revoked
    #
    # We need this to avoid permission issues in the containers.
    os.umask(0)

    JWT_ISSUER = os.getenv("JWT_ISSUER", KEYCLOAK_ISSUER)

    PUBLIC_KEY = retrieve_public_key()

    app = Flask(__name__)

    with app.app_context():
        for logger_name in logging.root.manager.loggerDict:
            if logger_name == "gunicorn.error":
                gunicorn_logger = logging.getLogger("gunicorn.error")
                app.logger.handlers = gunicorn_logger.handlers
                app.logger.setLevel(gunicorn_logger.level)

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

    app.config.from_mapping(
        CELERY=dict(
            broker_url="pyamqp://celery:123@rabbitmq/",
            result_backend="redis://redis",
            # task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    app.register_blueprint(bp)

    return app


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
