from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from time import gmtime, strftime
import re

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """View current portfolio of user"""
    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id",
        user_id=session["user_id"])[0]["cash"]
    stocks = get_user_portfolio()
    return render_template("index.html", stocks=stocks, cash=user_cash)
    

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        symbol = get_form_value(request, "symbol")
        shares = int(get_form_value(request, "shares"))
        lookup_result = lookup(symbol)
        # ensure valid symbol and amount of shares
        if not lookup_result or int(shares) < 1:
            return apology("Invalid symbol/share amount")
        else:
            user_cash = get_user_cash()
            # ensure that user can afford those shares
            if not user_cash >= (lookup_result["price"]*shares):
                return apology("You can't afford those shares")
            else:
                add_purchase_to_porfolio = db.execute(
                        """INSERT INTO portfolio(
                            user_id, symbol, shares, price, date, name)
                            VALUES (
                            :user_id, :symbol, :shares, :price, :date, :name)""", 
                            user_id=session["user_id"], symbol=symbol,
                            shares=shares, price=lookup_result["price"],
                            date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                            name=lookup_result["name"])
                if not add_purchase_to_porfolio:
                    return apology("Technical issues", "Try again later")
                else:
                    update_user_cash = db.execute(
                            """UPDATE users SET cash = :cash
                            WHERE id = :user_id""",
                            cash=user_cash - lookup_result["price"]*shares,
                            user_id=session["user_id"])
                    if not update_user_cash:
                        return apology("Technical issues", "Try again later")
                    else:
                        return redirect(url_for("index"))
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    user_portfolio_history = db.execute(
        """SELECT symbol, shares, price, date 
        FROM portfolio WHERE user_id = :user_id""", 
        user_id=session["user_id"])
    return render_template("history.html", transactions=user_portfolio_history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not get_form_value(request, "username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not get_form_value(request, "password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", 
            username=get_form_value(request, "username"))
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(
                get_form_value(request, "password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        lookup_result = lookup(get_form_value(request, "symbol"))
        # Ensure that valid symbol was submitted.
        if not lookup_result:
            return apology("Invalid stock symbol")
        else:
            return render_template(
                "lookup.html", name=lookup_result["name"],
                symbol=lookup_result["symbol"], price=lookup_result["price"])
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # If user reached route via POST (as by submitting a form via POST).
    if request.method == "POST":
        
        # Get content of submitted form.
        username = get_form_value(request, "username")
        password = get_form_value(request, "password")
        password_confirmation = get_form_value(request, "password-confirmation")
        
        # Check if form has no blank fields.
        if "" in (username, password, password_confirmation):
            return apology("Fill all the blanks")
        # Check if password and confirmation matches.
        elif password != password_confirmation:
            return apology("Password and confirmation", "They gotta be the same")
        else:
            # Ensure that provided username is unique.
            is_username_unique = db.execute("SELECT * FROM users WHERE username = :username", username=username)
            if not is_username_unique:
                # Hash password for security and insert form into DB.
                hash_password = pwd_context.hash(password)
                result = db.execute(
                        "INSERT INTO users (username, hash) VALUES (:username, :hash)",
                        username=username, hash=hash_password)
                # Check if record got saved in DB.
                if not result:
                    return apology("Technical issues", "Try again")
                else:
                    # Start session for registered user and log him in.
                    session["user_id"] = result
                    return redirect(url_for("index"))
            else:
                return apology("Username is not unique")
    # Return register form if user reached via GET.
    else:
        return render_template("register.html")
        
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    stocks = get_user_portfolio()
    if request.method == "POST":
        # Ensure that valid symbol and shares amount was submitted.
        try:
            symbol = get_form_value(request, "symbol")
            shares = int(get_form_value(request, "shares"))
        except ValueError:
            return apology("Invalid symbol/share amount")
        try:
            lookup_result = lookup(symbol)
        except AttributeError:
            return apology("Invalid symbol/share amount")
        user_cash = get_user_cash()
        if not lookup_result or int(shares) < 1:
            return apology("Invalid symbol/share amount")
        else:
            # Get amount of shares currently held by user.
            stock_in_portfolio = next(filter(
                lambda stock: stock["symbol"] == symbol, 
                get_user_portfolio()))
            # Ensure that user has enough shares to sell.
            if int(stock_in_portfolio["shares"]) < shares:
                return apology("You don't have so many shares!")
            else:
                # Update transactions history.
                add_sale_to_portfolio = db.execute(
                        """INSERT INTO portfolio(
                            user_id, symbol, shares, price, date, name)
                            VALUES (
                            :user_id, :symbol, :shares,
                            :price, :date, :name)""", 
                            user_id=session["user_id"], symbol=symbol,
                            shares=-shares, price=lookup_result["price"],
                            date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                            name=lookup_result["name"])
                if not add_sale_to_portfolio:
                    return apology("Technical issues", "Try again")
                else:
                    # Update user's cash.
                    user_cash = db.execute(
                            """UPDATE users SET cash = :cash 
                            WHERE id = :user_id""",
                            cash=user_cash+shares*int(lookup_result["price"]),
                            user_id=session["user_id"])
                    return redirect(url_for("index"))
    else:
        return render_template("sell.html", stocks=stocks)
        
@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit more cash than initial 10,000 $."""
    if request.method == "POST":
        cash_to_deposit = int(get_form_value(request, "cash"))
        # Ensure that proper amount of cash was submitted.
        if not cash_to_deposit > 0:
            return apology("Invalid cash deposit")
        else:
            # Update user's cash.
            user_cash = get_user_cash()
            deposit_cash = db.execute(
                "UPDATE users SET cash = :cash",
                cash=cash_to_deposit+user_cash)
            if not deposit_cash:
                return apology("Technical issues", "Try again")
            else:
                return redirect(url_for("index"))
    else:
        return render_template("deposit.html")

def get_user_portfolio():
    """Get current portfolio of user including name, 
    symbol, amount and price of shares.
    """
    user_portfolio = db.execute(
        "SELECT symbol, shares, name FROM portfolio WHERE user_id = :user_id", 
        user_id=session["user_id"])
    stocks = []
    # Sum up history to single record for each stock.
    for purchase in user_portfolio:
        if not any(purchase["symbol"] in stock["symbol"] for stock in stocks):
                stocks.append({"symbol": purchase["symbol"], 
                "shares": purchase["shares"], "name": purchase["name"],
                "price": lookup(purchase["symbol"])["price"]})
        else:
            for stock in stocks:
                if stock["symbol"] == purchase["symbol"]:
                    stock["shares"] += purchase["shares"]
    # Exclude elements that have non-positive share amount.
    stocks_in_portfolio = [stock for stock in stocks if not stock["shares"] == 0]
    return stocks_in_portfolio
    
def get_user_cash():
    """Get user's cash"""
    user_cash = db.execute(
                    "SELECT cash FROM users WHERE id = :user_id",
                    user_id=session["user_id"])[0]["cash"]
    if user_cash:
        return int(user_cash)
    else:
        return None

def remove_non_alpha(string):
    """Remove non-alphabetical characters to prevent SQL Injection Attack"""
    regex = re.compile("[^a-zA-Z0-9]")
    string = regex.sub("", string)
    return string

def get_form_value(request, name):
    """Save method to retrieve values from forms."""
    form_value = remove_non_alpha(request.form.get(name))
    return form_value
