import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, lookup_image

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

username = None

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///dictionary.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")




@app.route("/history")
@login_required
def history():
    #get user_id
    userId = session["user_id"]
    #get all the data we need from user
    results = db.execute("SELECT DISTINCT (word) FROM history WHERE id = ?", userId)



    display = []
    for r in results:
        word = r['word']

        word_in_dict = lookup(word)


        #append the values in the display list in form of dicts every dict corresponds to a stock
        display.append({'word':word, 'pronunciation': word_in_dict['pronunciation'], 'definitions': word_in_dict['definitions']})
    return render_template("history.html",results = display)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    #get user_id
    userId = session["user_id"]
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("index.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        word = request.form.get("word")
        if not word:
            return render_template("apology.html",message = "You should type a word")

        word_in_dict = lookup(word)
        if word_in_dict == None:
            message = "You should type a valid word"
            return render_template("apology.html",message = message)

        time = datetime.datetime.now()
        
        db.execute("INSERT INTO history (id, word, time) VALUES (?, ?, ?)", userId, word_in_dict['word'], time)

        results = lookup_image(word)['hits']

        

        return render_template("word.html",word = word_in_dict['word'],
                            pronunciation = word_in_dict['pronunciation'], definitions = word_in_dict['definitions'], results = results)


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return render_template("apology.html",message = "You should type an username")

        if len(username) < 5:
            return render_template("apology.html",message = "Your username should at least contain 5 characters")
        password = request.form.get("password")

        if not password:
            return render_template("apology.html",message = "You should type a password")

        if len(password) <6:
            print ('password is too short It must be at least 6 characters')

        valid_password = False
        #l, u, p, d = 0, 0, 0, 0
        if (len(password) >= 6):
            #//for i in password:

                # counting lowercase alphabets
                #if (i.islower()):
                    #l+=1

                # counting uppercase alphabets
                #if (i.isupper()):
                 #   u+=1

                # counting digits
                #if (i.isdigit()):
                 #   d+=1

                # counting the mentioned special characters
                #if(i=='@'or i=='$' or i=='_'):
                 #   p+=1
        #if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
            valid_password = True
        else:
            valid_password = False

        if valid_password:
            confirmation = request.form.get("confirmation")
            if not confirmation or confirmation != password:
                return render_template("apology.html",message = "You should type the same password")
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                    username = username, hash = password_hash)
            return render_template("login.html")
        else:
            return render_template("apology.html",message = "Your password should at least contain one uppercase, one lowercase and '@'or '$' or '_' or a number")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
