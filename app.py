from flask import Flask, request, render_template

app = Flask(__name__)

@app.get("/")
def hello_world():
    return render_template('index.html')

@app.post("/")
def build():
    print(request.form['git_repository_url'])
    return "<p>Hello, World!</p>"
