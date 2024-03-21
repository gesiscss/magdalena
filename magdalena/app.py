import os
import shutil

from flask import Flask, request, render_template, send_file

from .methodshub import MethodsHubHTTPContent, MethodsHubGitContent

app = Flask(__name__)

with app.app_context():
    if "MAGDALENA_SHARED_DIR" not in os.environ:
        app.logger.warning("MAGDALENA_SHARED_DIR is not defined! Using default.")
        os.environ["MAGDALENA_SHARED_DIR"] = "/tmp/magdalena-shared-volume"
    shared_root_dir = os.getenv("MAGDALENA_SHARED_DIR")
    app.logger.info("Shared directory is %s", shared_root_dir)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/")
def build():
    app.logger.info("Form content is %s", request.json)

    assert "source_url" in request.json, "Field source_url missing in form"

    if (
        "github.com" in request.json["source_url"]
        or "gitlab.com" in request.json["source_url"]
    ):
        assert "filename" in request.json, "Field filename missing in form"
        methods_hub_content = MethodsHubGitContent(
            request.json["source_url"],
            request.json["filename"],
            (
                request.json["forward_id"]
                if ("forward_id" in request.json and len(request.json["forward_id"]))
                else None
            ),
        )
    else:
        methods_hub_content = MethodsHubHTTPContent(
            request.json["source_url"],
            (
                request.json["forward_id"]
                if ("forward_id" in request.json and len(request.json["forward_id"]))
                else None
            ),
            (
                request.json["filename"]
                if ("filename" in request.json and len(request.json["filename"]))
                else None
            ),
        )

    assert methods_hub_content.clone_or_pull() is None, "Fail on clone or pull"
    assert methods_hub_content.create_container() is None, "Fail on container creation"
    assert (
        methods_hub_content.render_formats(request.json["target_format"]) is None
    ), "Fail on render contributions"

    if request.json["response"] == "download":
        app.logger.info("Sending response to user")
        if len(request.json["target_format"]) == 1:
            return send_file(
                methods_hub_content.rendered_file(request.json["target_format"][0]),
                mimetype="text/plain",
                as_attachment=True,
            )
        else:
            assert methods_hub_content.zip_all_formats() is None, "Fail on zip formats"

            return send_file(
                methods_hub_content.zip_file_path,
                mimetype="application/zip",
                as_attachment=True,
            )

    if request.json["response"] == "forward":
        app.logger.info(
            "Sending response to %s", os.getenv("MAGDALENA_GRAPHQL_TARGET_URL")
        )

        if len(request.json["target_format"]) == 1:
            methods_hub_content.push_rendered_formats(request.json["target_format"])
        else:
            methods_hub_content.push_all_rendered_formats()

        return {"status": "OK"}
