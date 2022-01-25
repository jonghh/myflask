from flask import Flask
from .view import hello

app = Flask(__name__)

app.register_blueprint(hello.bp_hello)