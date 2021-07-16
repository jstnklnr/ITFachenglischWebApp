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

@main.route('/exercise-selection')
def exercise_selection():
    return render_template("exercise_selection.html")

@main.route('/vocabulary-sel')
def vocabel_sel():
    session["exercise"] = "vocabulary"
    return redirect('/book-selection') 

@main.route('/audio')
def audio():
    session["exercise"] = "audio"
    
    return redirect("/amount") 

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
    num = len(namelist)
    headline = "Book"
    href = "selection"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href)

@main.route('/selection')
def selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    if not request.args.get("book"):
        return "failed"

    session["book"] = request.args.get("book")

    num = 0
    namelist = []
    headline = ""
    if "," in str(session['book']):
        session['selection'] = "topic"
        namelist = api.getTopics()
        num = len(namelist)
        headline = "Topic"
    else:
        session['selection'] = "unit"
        namelist = api.getUnits(session["book"])
        num = len(namelist)
        headline = "Unit"
    href="language"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href)

@main.route('/language')
def language():
    if session["exercise"] != "vocabulary" or session["exercise"] != "phrase":
       return render_template("home.html")

    if not request.args.get('topic') or request.args.get('unit'):
        return "failed"

    if session['selection'] == "topic":
        session['unit'] = request.args.get('topic')
    else:
        session['topic'] = request.args.get('unit')

    namelist = api.getLanguages()
    num = len(namelist)
    headline = "language"
    href = ""

    if session["exercise"] == "vocabulary":
        href = "vocabulary"
    else:
        href = "phrase"

    session['ready'] = True

    return render_template("selection.html", num=num, namelist=namelist, headline=headline)


@main.route('/amount')
def amount():
    if session["exercise"] != "vocabulary" and session["exercise"] != "phrase" and session["exercise"] != "audio":
        return render_template("home.html")

    if session["exercise"] != "audio":
        print(session["exercise"])

        if not request.args.get('language'):
                return "failed"

        session['language'] = request.args.get('language')
        session['started'] = True

    return render_template("amount.html")
############################################
#Exercise
############################################
@main.route('/vocabulary')
def vocabulary():
    if session['ready'] != True:
        return render_template("home.html")

    if session['vocabulary_test'] == []:
        return render_template("ready.html")

    if session['started']:
        session['started'] = False

        amount = 0
        if request.args.get('amount'):
            amount = request.args.get('amount')

        topic_or_unit = ""
        data = []
        if session['selection'] == "topic":
            topic_or_unit = session['topic'].split(",")
            data = api.getVocabulary(session['book'].split(","), language, amount, topic=topic_or_unit)
        else:
            topic_or_unit = session['unit'].split(",")
            data = api.getVocabulary([session['book']], language, amount, unit=topic_or_unit)
    
        session['vocabulary_test'] = data

    word = session['vocabulary_test'].pop()
    transLang = ""
    if session['language'] == "English":
        transLang = "German"
    else:
        transLang = "English"
    translation = api.getTranslation(word, session['language'], transLang)

    return render_template("vocabulary.html", word=word, translation=translation)

###########################################
#Sessions
###########################################
#
# 'exercise' string - name of the exercise vocabulary, phrase or audio
# 'book' string - name of book(s) 
# 'selection' string - unit or topic
# 'unit' string list - names of units
# 'topic' string list - names of topics
# 'ready' boolean - everything is selected
# 'started' boolean - only first time on vocabulary for api request
# 'vocabulary_test' list of dict - list of vocabulary, lenghts equals selected amount