# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from logging.config import dictConfig
import os

from celery import Celery
from celery import Task
from flask import Flask

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", None)
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", None)

assert CELERY_BROKER_URL is not None, "CELERY_BROKER_URL can't be None"
assert CELERY_BACKEND_URL is not None, "CELERY_BACKEND_URL can't be None"

# Define the logging level
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
LOGGING_LEVEL = LOGGING_LEVEL.upper()

# Logging level must be one of the defined in https://docs.python.org/3/howto/logging.html#logging-levels
assert LOGGING_LEVEL in [
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
], "Logging level is invalid"

# Configuring the logging
#
# https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",  # https://docs.python.org/3/library/logging.config.html#access-to-external-objects
            },
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console"],
                "level": LOGGING_LEVEL,
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"],
                "level": LOGGING_LEVEL,
                "propagate": False,
            },
        },
        "root": {"level": LOGGING_LEVEL, "handlers": ["console"]},
    }
)


def create_app():
    from .views import bp

    app = Flask(__name__)

    app.config.from_mapping(
        CELERY=dict(
            broker_url=CELERY_BROKER_URL,
            result_backend=CELERY_BACKEND_URL,
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
