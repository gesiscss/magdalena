# SPDX-FileCopyrightText: 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from celery.result import AsyncResult

from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response
from flask import stream_with_context

# import tasks

bp = Blueprint("tasks", __name__)


@bp.route("/keycloak.min.js")
def send_keycloak_adapter():
    return send_from_directory("/var/keycloak", "keycloak.min.js")


@bp.get("/result/<id>")
def result(id):
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


# To debug,
#
# @stream_with_context
# def poll_result(id):
#     current_app.logger.error(result)
@stream_with_context
def poll_result(id):
    # This is a generator and yield should be used to return data
    result = AsyncResult(id)

    while result.state != "SUCCESS":
        data = {"state": result.state, "info": result.info}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

        # Update for while
        result = AsyncResult(id)
        current_app.logger.error(result.parent)

    if result.state == "SUCCESS":
        data = {"state": result.state, "info": result.info, "result": result.result}
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
    keycloak_scheme = os.getenv("FRONTEND_KEYCLOAK_SCHEME", None)
    if keycloak_scheme is None:
        keycloak_scheme = os.getenv("KEYCLOAK_SCHEME", None)

    keycloak_domain = os.getenv("FRONTEND_KEYCLOAK_DOMAIN", None)
    if keycloak_domain is None:
        keycloak_domain = os.getenv("KEYCLOAK_DOMAIN", None)

    return render_template(
        "index.html",
        keycloak_scheme=keycloak_scheme,
        keycloak_domain=keycloak_domain,
        keycloak_realm=KEYCLOAK_REALM,
        keycloak_client=KEYCLOAK_CLIENT,
    )


@bp.post("/")
def build():
    authorization = request.headers.get("Authorization")
    assert authorization, "Authorization is missing in header"

    authorization_scheme, authorization_token = authorization.split()
    assert authorization_scheme == "Bearer", "Authorization is missing in header"

    app.logger.debug("Validating JWT")
    app.logger.debug("\tExpected issuer: %s", JWT_ISSUER)
    app.logger.debug("\tJWT: %s", authorization_token)

    jwt.decode(
        authorization_token,
        key=PUBLIC_KEY,
        algorithms=["RS256"],
        options={"verify_aud": False},
        issuer=JWT_ISSUER,
    )

    app.logger.info("Form content is %s", request.json)

    assert "source_url" in request.json, "Field source_url missing in form"

    assert "response" in request.json, "Field response missing in form"

    assert request.json["response"] in [
        "download",
        "forward",
    ], "Field response is invalid"

    response_type = request.json["response"]

    if response_type == "forward":
        assert "forward_id" in request.json, "Field forward_id missing in form"

        assert request.json["forward_id"], "Field forward_id is invalid"

        forward_id = request.json["forward_id"]
    else:
        forward_id = None

    if (
        "github.com" in request.json["source_url"]
        or "gitlab.com" in request.json["source_url"]
    ):
        # assert "filename" in request.json, "Field filename missing in form"
        if "filename" not in request.json or len(request.json["filename"]) == 0:
            app.logger.warning("filename is not defined or empty! Using 'README.md'")
            filename = "README.md"
        else:
            filename = request.json["filename"]

        # assert "git_commit_id" in request.json, "Field git_commit_id missing in form"
        if (
            "git_commit_id" not in request.json
            or len(request.json["git_commit_id"]) == 0
        ):
            app.logger.warning("git_commit_id is not defined or empty!")
            git_commit_id = None
        else:
            git_commit_id = request.json["git_commit_id"]

        methods_hub_content = MethodsHubGitContent(
            request.json["source_url"],
            id_for_graphql=forward_id,
            git_commit_id=git_commit_id,
            filename=filename,
        )
    else:
        methods_hub_content = MethodsHubHTTPContent(
            request.json["source_url"],
            id_for_graphql=forward_id,
            filename=(
                request.json["filename"]
                if ("filename" in request.json and len(request.json["filename"]))
                else None
            ),
        )

    try:
        methods_hub_content.clone_or_pull()
    except Exception as error:
        app.logger.error("Error when cloning\n\t%s", error)
        return {"message": str(error)}, 500

    try:
        methods_hub_content.create_container()
    except Exception as error:
        app.logger.error("Error when creating container\n\t%s", error)
        return {"message": str(error)}, 500

    try:
        methods_hub_content.render_formats(request.json["target_format"])
    except Exception as error:
        app.logger.error("Error when rendering\n\t%s", error)
        return {"message": str(error)}, 500

    if response_type == "download":
        app.logger.info("Sending response to user")
        if len(request.json["target_format"]) == 1:
            return (
                send_file(
                    methods_hub_content.rendered_file(request.json["target_format"][0]),
                    mimetype="text/plain",
                    as_attachment=True,
                ),
                201,
            )
        else:
            assert methods_hub_content.zip_all_formats() is None, "Fail on zip formats"

            return (
                send_file(
                    methods_hub_content.zip_file_path,
                    mimetype="application/zip",
                    as_attachment=True,
                ),
                201,
            )

    if response_type == "forward":
        app.logger.info(
            "Sending response to %s", os.getenv("MAGDALENA_GRAPHQL_TARGET_URL")
        )

        if len(request.json["target_format"]) == 1:
            methods_hub_content.push_rendered_formats(
                request.json["target_format"], authorization_token
            )
        else:
            methods_hub_content.push_all_rendered_formats(authorization_token)

        return {"status": "OK"}, 201
