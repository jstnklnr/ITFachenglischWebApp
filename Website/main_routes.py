from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import flash
from flask import url_for

from api_interface import Api
from util import getWordAmount
from util import addSpecificKeyValueToList

main = Blueprint('main', __name__)
api = Api("https://localhost:5000")

############################################
#Main
############################################
@main.route('/')
def index():
    return render_template("index.html")

@main.route('/exercise-selection')
def exercise_selection():
    return render_template("exercise.html")

@main.route('/vocabulary-sel')
def vocabel_sel():
    session["exercise"] = "vocabulary"
    return redirect('/book-selection') 

@main.route('/audio-sel') #TODO
def audio_sel():
    session["exercise"] = "audio"
    return redirect("/amount") 

@main.route('/phrase-sel')  #TODO
def phrase_sel():
    session["exercise"] = "phrase"
    return redirect('/language')  


############################################
#Selection
############################################
@main.route('/book-selection')
def book_selection():
    if session["exercise"] != "vocabulary":
        return render_template("index.html")

    namelist = api.getBooks()
    headline = "Select your book"
    href = "selection"

    return render_template("selection.html", num=len(namelist), namelist=namelist, headline=headline, href=href, selection_type="book")

@main.route('/selection')
def selection():
    if session["exercise"] != "vocabulary":
        return render_template("index.html")

    if not request.args.get("book"):
        return "failed"

    session["book"] = request.args.get("book")

    num = 0
    namelist = []
    headline = ""
    if "," in str(session['book']):
        session['selection'] = "topic"
        namelist = addSpecificKeyValueToList(api.getTopics(), "topic")
        session['unit_topic_list'] = namelist
        session['amount_list'] = addSpecificKeyValueToList(api.getTopics(), "amount")
        num = len(namelist)
        headline = "Topic"
    else:
        session['selection'] = "unit"
        namelist = addSpecificKeyValueToList(api.getUnits(session["book"]), "unit")
        session['unit_topic_list'] = namelist
        session['amount_list'] = addSpecificKeyValueToList(api.getUnits(session["book"]), "amount")
        num = len(namelist)
        headline = "Unit"
    href="language"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href, selection_type=session["selection"])

@main.route('/language')
def language():
    if session["exercise"] != "vocabulary" and session["exercise"] != "phrase":
       return render_template("index.html")
    
    if not request.args.get('topic') and not request.args.get('unit'):
        return redirect("selection")

    if session['selection'] == "topic":
        session['topic'] = request.args.get('topic')
        session['max_amount'] = getWordAmount(session['unit_topic_list'], session['amount_list'], session['topic'].split(","))

    else:
        session['unit'] = request.args.get('unit')
        session['max_amount'] = getWordAmount(session['unit_topic_list'], session['amount_list'], session['unit'].split(","))

    namelist = api.getLanguages()
    num = len(namelist)
    headline = "Select your language"
    href = "amount"

    """
    if session["exercise"] == "vocabulary":
        href = "vocabulary"
    else:
        href = "phrase"
        """

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href, selection_type="language")

@main.route('/amount')
def amount():
    if session["exercise"] != "vocabulary" and session["exercise"] != "phrase" and session["exercise"] != "audio":
        return render_template("index.html")

    href = ""
    if session["exercise"] == "vocabulary":
        if not request.args.get('language'):
                return redirect("language")
        session['language'] = request.args.get('language')
        href = "vocabulary"
    elif session["exercise"] == "audio":
        href = "audio"

    session['ready'] = True
    session['started'] = True
    headline = "Select your amount"
        
    return render_template("selection.html", headline=headline, href=href, selection_type="amount", amount=session['max_amount'])

############################################
#Exercise
############################################
@main.route('/vocabulary')
def vocabulary():
    if not session['ready'] or session['exercise'] != "vocabulary":
        return render_template("index.html")

    if session['started']:
        session['count'] = 0
        session['test_data'] = []
        session['started'] = False

        amount = 0
        if not request.args.get('amount'):
            return redirect("amount")

        amount = request.args.get('amount')    

        topic_or_unit = []
        data = []
        if session['selection'] == "topic":
            topic_or_unit = session['topic'].split(",")
            data = api.getVocabulary(session['book'].split(","), session['language'], amount, topic=topic_or_unit)
        else:
            topic_or_unit = session['unit'].split(",")
            data = api.getVocabulary(session['book'].split(","), session['language'], amount, unit=topic_or_unit)
    
        session['test_data'] = data

    if session['test_data'] == []:
        return render_template("index.html")

    word = session['test_data'][len(session['test_data']) - 1]
    session['current'] = word

    trans_lang = ""
    if session['language'] == "English":
        trans_lang = "German"
    else:
        trans_lang = "English"

    session['translation'] = api.getTranslation(word, session['language'], trans_lang)
    session['test_data'].pop()

    return render_template("selection.html", word=word, selection_type="vocabulary", headline="", href="#")

@main.route('/audio')
def audio():
    if not session['ready'] or session['exercise'] != "audio":
        return render_template("index.html")

    if session['started']:
        session['test_data'] = []
        session['started'] = False

        amount = 0
        if request.args.get('amount'):
            return redirect("amount")

        amount = request.args.get('amount')

        data = api.getAudio(session['language'], amount)
        session['test_data'] = data

    if session['test_data'] == []:
        return render_template("index.html")

    phrase = session['test_data'].pop()
    session['current'] = phrase
        
    return render_template("selection.html", phrase=phrase, selection_type="audio", headline="", href="#")

###########################################
#Util Route
###########################################
@main.route("/check", methods=['POST'])
def check():
    if not request.get_json():
        return 400

    translation = request.get_json()['translation'].replace("-", " ").strip().lower()
    found_translation = False

    if translation.startswith("to "):
        translation = translation[2:]

    if translation.endswith(" to"):
        translation = translation[0: -2]

    item = translation.replace(" ", "")
    print(translation);

    for item in session['translation']:
        item = item.strip().lower()

        if item.startswith("to "):
            item = item[2:]

        if item.endswith(" to"):
            item = item[0: -2]

        item = item.replace(" ", "")
        print(item)

        if translation == item:
            found_translation = True

    session['checked'] = True

    if not found_translation:
        return {"Success": False, "Translations": session["translation"]}, 200

    session['count'] += 1

    return {"Success": True, "Translations": session["translation"] }, 200

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
# 'test_data' list of dict - list of data (vocabulary or audio), length equals selected amount 
# 'translation' string - translation for the word in vocabulary
# 'current' string - current word or phrase
# 'count' int - number of right answers
# 'max_amount' int - get the max amount of exercises
# 'amount_list' list - temporary cache to get the max amount for the exercise
# 'unit_topic_list' list - temporary cache to get the max amount for the exercise