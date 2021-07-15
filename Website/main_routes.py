from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("home.html")

@main.route('/exercise-selection')
def exercise_selection():
    return render_template("exercise_selection.html")

@main.route('/vocabel-test')
def vocabel_test():
    session["exercise"] = "vocabulary"
    return render_template("vocabel_test.html")

@main.route('/audio')
def audio():
    session["exercise"] = "audio"
    return "hallo"

@main.route('/phrase')
def phrase():
    session["exercise"] = "phrase"
    return "hallo"



@main.route('/book-selection')
def book_selection():
    return "hallo"

@main.route('/topic-selection')
def topic_selection():
    session["exercise"] = request.args.get("exercise")
    return render_template("topic_selection.html")

