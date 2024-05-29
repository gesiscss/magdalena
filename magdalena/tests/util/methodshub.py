def expected_mybinder_build_response(image, repository, commit_id):
    return f"""
data: {{"phase": "built", "imageName": "{image}:{commit_id}", "message": "Found built image, launching...\\n"}}
data: {{"phase": "ready", "message": "server running at https://notebooks.gesis.org/binder/jupyter/user/gesis-methods-hub-gejw8fu0/\\n", "image": "{image}:{commit_id}", "repo_url": "https://github.com/GESIS-Methods-Hub/{repository}", "token": "qKcb4Ja4Q12TqaR7zb8Tog", "binder_ref_url": "https://github.com/GESIS-Methods-Hub/{repository}/tree/{commit_id}", "binder_launch_host": "https://mybinder.org/", "binder_request": "v2/gh/GESIS-Methods-Hub/{repository}/{commit_id}", "binder_persistent_request": "v2/gh/GESIS-Methods-Hub/{repository}/{commit_id}", "url": "https://notebooks.gesis.org/binder/jupyter/user/gesis-methods-hub-gejw8fu0/"}}
"""
