from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect

from api_interface import Api

main = Blueprint('main', __name__)
api = Api("https://localhost:5000")

@main.route('/')
def index():
    return render_template("home.html")

@main.route('/exercise-selection')
def exercise_selection():
    return render_template("exercise_selection.html")

@main.route('/vocabulary')
def vocabel_test():
    session["exercise"] = "vocabulary"
    return redirect('/book-selection') 

@main.route('/audio') #TODO
def audio():
    session["exercise"] = "audio"
    return "hallo" 

@main.route('/phrase') #TODO
def phrase():
    session["exercise"] = "phrase"
    return "hallo" 


@main.route('/book-selection') #TODO
def book_selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    bookNames = api.getBooks()
        
    return "hallo" #return all books in html

@main.route('/selection')
def topic_selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    session["book"] = request.args.get("book")

    num = 0
    namelist = []
    sel = ""
    if "+" in str(session['book']):
        namelist = api.getTopics()
        num = len(topicNames)
        sel = "Topic"
    else:
        namelist = api.getUnits(session["book"])
        num = len(unitNames)
        sel = "Unit"
    
    return render_template("selection.html", num = num, namelist = namelist, sel = sel)

