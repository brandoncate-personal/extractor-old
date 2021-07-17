import flask
from handlers import extractor


"""
    Because the google cloud function runtime for python sucks you have to define a main.py file
    As such all handlers need to be defined here
    Try to keep all logic out of this file and instead write it as its own function in the handlers/ package
"""


def extract(request: flask.Request) -> flask.Response:
    return extractor.extract(request)
