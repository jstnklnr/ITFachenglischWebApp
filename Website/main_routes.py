from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("home.html")

@main.route('/exercise-selection')
def exercise_selection():
    return render_template("exercise_selection.html")

@main.route('/vocabulary') #TODO
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

    #sql get book names
        
    return "hallo" #return all books in html

@main.route('/selection') #TODO
def topic_selection():
    if session["exercise"] != "vocabulary":
        return render_template("home.html")

    session["book"] = request.args.get("book")

    if "+" in str(session['book']):
        #api get book topics
        #num = len of list
        pass
    else:
        #api get book units
        #num = len of list
        pass

    num = 0
    namelist = []
    
    return render_template("topic_selection.html", num = num, namelist = namelist)


