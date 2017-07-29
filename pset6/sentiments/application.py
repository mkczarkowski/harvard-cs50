from flask import Flask, redirect, render_template, request, url_for

import os
import sys

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    # If user doesn't exist / has private account - redirect to start page.
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if not tweets:
        return redirect(url_for("index"))
    
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # Instantiate analyzer.
    analyzer = Analyzer(positives, negatives)
    positive, negative, neutral = 0.0, 0.0, 100.0
    
    # Get percentage of sentiment for each word in a tweet.
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            positive += 100 / len(tweets);
        elif score < 0.0:
            negative += 100 / len(tweets);
        else:
            neutral += 100 / len(tweets);
            
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
