import os
import shutil

from flask import Flask, request, render_template, send_file

from .methodshub import MethodsHubContent

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

    methods_hub_content = MethodsHubContent(
        request.form["git_repository_url"], request.form["filename"]
    )
    assert methods_hub_content.clone_or_pull(), "Fail on clone or pull"
    assert methods_hub_content.create_container(), "Fail on container creation"
    assert methods_hub_content.render_all_formats(), "Fail on render contributions"
    assert methods_hub_content.zip_all_formats(), "Fail on zip formats"

    return send_file(
        methods_hub_content.zip_filename, mimetype="application/zip", as_attachment=True
    )
