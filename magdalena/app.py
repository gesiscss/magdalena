# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from celery import Celery
from celery import Task
from flask import Flask


def create_app():
    import logging

    from .views import bp

    app = Flask(__name__)

    with app.app_context():
        for logger_name in logging.root.manager.loggerDict:
            if logger_name == "gunicorn.error":
                gunicorn_logger = logging.getLogger("gunicorn.error")
                app.logger.handlers = gunicorn_logger.handlers
                app.logger.setLevel(gunicorn_logger.level)

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
