from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect

from api_interface import Api

main = Blueprint('main', __name__)
api = Api("https://localhost:5000")

############################################
#Main
############################################
@main.route('/')
def index():
    return render_template("home.html")

@main.route('/vocabulary-sel')
def vocabel_sel():
    session["exercise"] = "vocabulary"
    return redirect('/book-selection') 

@main.route('/audio') #TODO
def audio():
    session["exercise"] = "audio"
    return "hallo" 

@main.route('/phrase-sel')
def phrase_sel():
    session["exercise"] = "phrase"
    return redirect('/language')  


############################################
#Selection
############################################
@main.route('/book-selection')
def book_selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    namelist = api.getBooks()
    num = len(bookNames)
    headline = "Book"

    href = "selection"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href)

@main.route('/selection')
def selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    session["book"] = request.args.get("book")

    num = 0
    namelist = []
    headline = ""
    if "+" in str(session['book']):
        session['selection'] = "topic"
        namelist = api.getTopics()
        num = len(topicNames)
        headline = "Topic"
    else:
        session['selection'] = "unit"
        namelist = api.getUnits(session["book"])
        num = len(unitNames)
        headline = "Unit"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline)

@main.route('/language')
def language():
    if session["exercise"] != "vocabulary" or session["exercise"] != "phrase":
       return render_template("home.html") 

    namelist = api.getLanguages()
    num = len(langList)
    headline = "language"
    href = ""

    if session["exercise"] == "vocabulary":
        href = "vocabulary"
    else:
        href = "phrase"

    session['ready'] = True

    return render_template("selection.html", num=num, namelist=namelist, headline=headline)


############################################
#Exercise
############################################
@main.route('/vocabulary')
def vocabulary():
    if session['ready'] != True:
        return render_template("home.html")

    language = request.args.get('language')
    return 'ok'