from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import flash
from flask import jsonify

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

@main.route('/audio-sel')
def audio_sel():
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
    if session["exercise"] != "vocabulary" and session["exercise"] != "phrase":
       return render_template("home.html")
    
    if not request.args.get('topic') and not request.args.get('unit'):
        return "failed"

    if session['selection'] == "topic":
        session['topic'] = request.args.get('topic')
    else:
        session['unit'] = request.args.get('unit')

    namelist = api.getLanguages()
    num = len(namelist)
    headline = "language"
    href = "amount"

    if session["exercise"] == "vocabulary":
        href = "vocabulary"
    else:
        href = "phrase"

    return render_template("selection.html", num=num, namelist=namelist, headline=headline, href=href)


@main.route('/amount')
def amount():
    if session["exercise"] != "vocabulary" and session["exercise"] != "phrase" and session["exercise"] != "audio":
        return render_template("home.html")

    href = ""
    if session["exercise"] == "vocabulary":

        if not request.args.get('language'):
                return "failed"

        session['language'] = request.args.get('language')
        href = "vocabulary"
    elif session["exercise"] == "audio":
        href = "audio"

    session['ready'] = True
    session['started'] = True
        
    return "amount"#render_template("amount.html", href=href)


############################################
#Exercise
############################################
@main.route('/vocabulary')
def vocabulary():
    if not session['ready'] or session['exercise'] != "vocabulary":
        print(session['ready'])
        print(session['exercise'])
        return render_template("home.html")

    if session['started']:
        session['test_data'] = []
        session['started'] = False

        amount = 0
        if not request.args.get('amount'):
            return "failed"

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
        return render_template("home.html")

    word = session['test_data'][len(session['test_data']) - 1]
    session['current'] = word

    trans_lang = ""
    if session['language'] == "English":
        trans_lang = "German"
    else:
        trans_lang = "English"
    session['translation'] = api.getTranslation(word, session['language'], trans_lang)

    if not session['checked']:
        return render_template("vocabulary.html", word=word, trans_lang=trans_lang)

    session['test_data'].pop()
    session['checked'] = False
    

    trans_lang = ""
    if session['language'] == "English":
        trans_lang = "German"
    else:
        trans_lang = "English"

    return render_template("vocabulary.html", word=word, trans_lang=trans_lang)


@main.route('/audio')
def audio():
    if not session['ready'] or session['exercise'] != "audio":
        return render_template("home.html")

    if session['started']:
        session['test_data'] = []
        session['started'] = False

        amount = 0
        if request.args.get('amount'):
            return "failed"

        amount = request.args.get('amount')

        data = api.getAudio(session['language'], amount)
        session['test_data'] = data

    if session['test_data'] == []:
        return render_template("home.html")

    phrase = session['test_data'][len(session['test_data']) - 1]
    session['current'] = phrase

    trans_lang = ""
    if session['language'] == "English":
        trans_lang = "German"
    else:
        trans_lang = "English"

    if not session['checked']:
        return render_template("audio.html", phrase=phrase, trans_lang=trans_lang) #TODO

    session['checked'] = False
    session['test_data'].pop()
        
    return render_template("audio.html", phrase=phrase, trans_lang=trans_lang) #TODO

###########################################
#Util Route
###########################################
@main.route("/check", methods=['POST'])
def check():
    if not request.get_data() or not request.get_json():
        flash("Sorry, something went wrong. Please try again.")

        if session['exercise'] == "vocabulary":
                return redirect("/vocabulary")
        else:
            return redirect("/vocabulary") #TODO /audio

    translation = request.get_json()['translation']

    for item in session['translation']:
        if not (translation.strip()).lower() == (item.strip()).lower():
            flash("Wrong translation")
            
            print(item)

            if session['exercise'] == "vocabulary":
                return redirect("/vocabulary")
            else:
                return redirect("/vocabulary") #TODO /audio

    if session['exercise'] == "vocabulary":
        session['checked'] = True
        return redirect("/vocabulary")
    elif session['exercise'] == "audio":
        session['checked'] = True
        return redirect("/audio")
    else:
        return redirect("/")

###########################################
#Sessions
###########################################

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
# 'checked' boolean - when translation is true