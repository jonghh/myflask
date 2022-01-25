from flask import Blueprint, render_template

bp_hello = Blueprint("hello", __name__, url_prefix="/", static_folder="static")

@bp_hello.route("/")
def ask1():
    return render_template("hello.html")

@bp_hello.route("/analysis")
def ask2():
    return render_template("analysis.html")