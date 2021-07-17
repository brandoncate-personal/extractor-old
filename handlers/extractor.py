from git import Repo
import flask
import os
import shutil
import frontmatter


def extract(request: flask.Request) -> flask.Response:
    path = "tmp"

    repoName = request.args["repo"]

    if repoName is None or repoName == "":
        return f"empty repo query paramater"

    # make sure working dir is empty
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    repo = Repo.clone_from(repoName, path)

    markdown = []  # object holding unique set of .md files
    for filePath in repo.active_branch.commit.stats.files.keys():
        if filePath.endswith(".md"):
            post = frontmatter.load(path + '/' + filePath)

            markdown.append({
                'path': filePath,
                'title': post['title']
            })

    repo.close()

    data = {
        "repo": repoName,
        "branch": repo.active_branch.name,
        "data": list(markdown)
    }

    response = flask.jsonify(data)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')

    return response
