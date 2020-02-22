from flask import Flask 

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base View."""
    message = "hi"
    return message 