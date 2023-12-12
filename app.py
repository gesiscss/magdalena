import os
import shutil

from flask import Flask, request, render_template, send_file

from .methodshub import MethodsHubHTTPContent, MethodsHubGitContent

app = Flask(__name__)

with app.app_context():
    if "MAGDALENA_SHARED_DIR" not in os.environ:
        app.logger.warn("MAGDALENA_SHARED_DIR is not defined! Using default.")
        os.putenv("MAGDALENA_SHARED_DIR", "/tmp/magdalena-shared-volume")
    shared_root_dir = os.getenv("MAGDALENA_SHARED_DIR")
    app.logger.info("Shared directory is %s", shared_root_dir)
    for dir_name in ("docker-scripts", "pandoc-filters"):
        app.logger.info("Copying %s to %s", dir_name, shared_root_dir)
        shutil.copytree(
            dir_name, os.path.join(shared_root_dir, dir_name), dirs_exist_ok=True
        )


@app.get("/")
def hello_world():
    return render_template("index.html")


@app.post("/")
def build():
    app.logger.info("Form content is %s", request.json)

    assert "source_url" in request.json, "Field source_url missing in form"

    if (
        "github.com" in request.json["source_url"]
        or "gitlab.com" in request.json["source_url"]
    ):
        assert "filename" in request.form, "Field filename missing in form"
        methods_hub_content = MethodsHubGitContent(
            request.json["source_url"], request.json["filename"]
        )
    else:
        methods_hub_content = MethodsHubHTTPContent(
            request.json["source_url"],
            request.json["filename"]
            if ("filename" in request.json and len(request.json["filename"]))
            else None,
        )

    assert methods_hub_content.clone_or_pull() is None, "Fail on clone or pull"
    assert methods_hub_content.create_container() is None, "Fail on container creation"
    assert (
        methods_hub_content.render_formats(request.json["target_format"]) is None
    ), "Fail on render contributions"

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
