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
    app.logger.info("Form content is %s", request.form)

    assert "source_url" in request.form, "Field source_url missing in form"

    if (
            'github.com' in request.form["source_url"] or
            'gitlab.com' in request.form["source_url"]
    ):
        assert "filename" in request.form, "Field filename missing in form"
        methods_hub_content = MethodsHubGitContent(
            request.form["source_url"], request.form["filename"]
        )
    else:
        methods_hub_content = MethodsHubHTTPContent(
            request.form["source_url"],
            request.form["filename"] if ("filename" in request.form and len(request.form["filename"])) else None
        )

    assert methods_hub_content.clone_or_pull() is not None, "Fail on clone or pull"
    assert methods_hub_content.create_container() is not None, "Fail on container creation"
    assert methods_hub_content.render_all_formats() is not None, "Fail on render contributions"
    assert methods_hub_content.zip_all_formats() is not None, "Fail on zip formats"

    return send_file(
        methods_hub_content.zip_file_path,
        mimetype="application/zip",
        as_attachment=True,
    )
