from flask import Flask, request, render_template

from methodshub import MethodsHubContent

app = Flask(__name__)


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

    return "<p>Hello, World!</p>"
