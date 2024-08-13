# SPDX-FileCopyrightText: 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import json
import os
import time

from celery.result import AsyncResult

from flask import Blueprint
from flask import request, render_template, send_file, send_from_directory
from flask import Response
from flask import current_app
from flask import stream_with_context

import jwt

from .pem import (
    KEYCLOAK_REALM,
    KEYCLOAK_CLIENT,
    KEYCLOAK_ISSUER,
    retrieve_public_key,
)

from . import tasks

authorization_required_from_env = os.getenv("AUTHORIZATION_REQUIRED", True)
if isinstance(authorization_required_from_env, str):

    authorization_required_from_env = authorization_required_from_env.lower()
    if authorization_required_from_env == "false":
        AUTHORIZATION_REQUIRED = False
    elif authorization_required_from_env == "true":
        AUTHORIZATION_REQUIRED = True
    else:
        AUTHORIZATION_REQUIRED = True
else:
    AUTHORIZATION_REQUIRED = authorization_required_from_env


bp = Blueprint("tasks", __name__)


@bp.route("/keycloak.min.js")
def send_keycloak_adapter():
    return send_from_directory("/var/keycloak", "keycloak.min.js")


@bp.get("/download/<id>")
def download(id):
    result = AsyncResult(id)

    if result.ready() and result.successful():
        file_path = result.result
        if file_path:
            if file_path.endswith(".zip"):
                return send_file(
                    file_path,
                    mimetype="application/zip",
                    as_attachment=True,
                )
            elif file_path.endswith(".html"):
                return send_file(
                    file_path,
                    mimetype="text/html",
                    as_attachment=False,
                )
            else:
                return send_file(
                    file_path,
                    mimetype="text/plain",
                    as_attachment=False,
                )

    return "Not found", 404


@bp.get("/result/<id>")
def result(id):
    result = AsyncResult(id)
    ready = result.ready()
    current_app.logger.debug("Async Task ready() is %s", ready)

    successful = None
    if ready:
        successful = result.successful()
        current_app.logger.debug("Async Task successful() is %s", successful)

    payload = None
    if ready and successful:
        payload = result.result

    return {
        "ready": ready,
        "successful": successful,
        "value": payload,
    }


# To debug,
#
# @stream_with_context
# def poll_result(id):
#     current_current_app.logger.error(result)
@stream_with_context
def poll_result(id):
    # This is a generator and yield should be used to return data
    result = AsyncResult(id)

    while result.state not in ["SUCCESS", "FAILURE"]:
        data = {"state": result.state}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(30)

        # Update for while
        result = AsyncResult(id)

    if result.state == "SUCCESS":
        data = {"state": result.state, "result": result.result}
        yield f"data: {json.dumps(data)}\n\n"
    else:
        data = {"state": result.state}
        yield f"data: {json.dumps(data)}\n\n"

    # Connection ends here.


@bp.get("/sse/result/<id>")
def result_sse(id):
    return Response(poll_result(id), mimetype="text/event-stream")


@bp.get("/")
def index():
    if AUTHORIZATION_REQUIRED:
        keycloak_scheme = os.getenv("FRONTEND_KEYCLOAK_SCHEME", None)
        if keycloak_scheme is None:
            keycloak_scheme = os.getenv("KEYCLOAK_SCHEME", None)
        current_app.logger.debug("keycloak_scheme = %s", keycloak_scheme)

        keycloak_domain = os.getenv("FRONTEND_KEYCLOAK_DOMAIN", None)
        if keycloak_domain is None:
            keycloak_domain = os.getenv("KEYCLOAK_DOMAIN", None)
        current_app.logger.debug("keycloak_domain = %s", keycloak_domain)

        return render_template(
            "index-authorization-required.html",
            keycloak_scheme=keycloak_scheme,
            keycloak_domain=keycloak_domain,
            keycloak_realm=KEYCLOAK_REALM,
            keycloak_client=KEYCLOAK_CLIENT,
        )

    return render_template("index.html")


@bp.post("/")
def build():
    if AUTHORIZATION_REQUIRED:
        JWT_ISSUER = os.getenv("JWT_ISSUER", KEYCLOAK_ISSUER)

        PUBLIC_KEY = retrieve_public_key()

        authorization = request.headers.get("Authorization")
        assert authorization, "Authorization is missing in header"

        authorization_scheme, authorization_token = authorization.split()
        assert authorization_scheme == "Bearer", "Authorization is missing in header"

        current_app.logger.debug("Validating JWT")
        current_app.logger.debug("\tExpected issuer: %s", JWT_ISSUER)
        current_app.logger.debug("\tJWT: %s", authorization_token)

        jwt.decode(
            authorization_token,
            key=PUBLIC_KEY,
            algorithms=["RS256"],
            options={"verify_aud": False},
            issuer=JWT_ISSUER,
        )

    celery_result = tasks.build.delay(request.json)
    return {"id": celery_result.id}
