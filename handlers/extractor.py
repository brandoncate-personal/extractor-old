from logging import error
from git import Repo, GitError
import flask
import os
import shutil
import frontmatter
import requests


def extract(repoName: str) -> flask.Response:
    path = "tmp"

    if repoName is None or repoName == "":
        return f"empty repo query paramater"

    # verify repo is reachable -- private repos not currently supported
    resp = requests.get(repoName)

    if resp.status_code == requests.codes.not_found:
        data = {
            "error": "unable to find repo " + repoName + " please verify repo exists and is public. Private repos are not currently supported",
        }

        response = flask.jsonify(data)
        response.status_code = requests.codes.not_found
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST')

        return response

    # make sure working dir is empty
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    repo = None
    try:
        repo = Repo.clone_from(repoName, path)
    except GitError as err:
        print("error has occurred")
        print(err)

    markdown = []  # object holding unique set of .md files

    # for now just use active branch which will normally be 'main'
    name = repo.active_branch.name
    for blob in repo.commit(name).tree.traverse():
        if blob.name.endswith(".md"):
            post = frontmatter.load(path + '/' + blob.path)

            if 'title' in post:
                markdown.append({
                    'path': blob.path,
                    'title': post['title']
                })
            else:
                # eventually could log useful error message to user
                # for now skip
                continue

    repo.close()

    data = {
        "repo": repoName,
        "branch": repo.active_branch.name,
        "data": list(markdown)
    }

    # add warning if no qualifying markdown found
    if len(markdown) == 0:
        data['warning'] = "no qualifying markdown found in repo " + repoName + \
            " please verify any markdown has a title field in frontmatter."

    response = flask.jsonify(data)
    response.status_code = requests.codes.ok
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')

    return response
