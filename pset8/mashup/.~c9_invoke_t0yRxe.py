import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from operator import itemgetter
from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    # Get value of geo parameter.
    geo = request.args.get("geo")
    # Ensure that geo is valid.
    if not geo:
        raise RuntimeError("Please enter value for geo parameter")
    geo_lookup = lookup(geo)
    # Return lookup for given geo as JSON.
    return jsonify(geo_lookup)

@app.route("/search")
def search():
    """Search for places that match query."""
    # Get value of query parameter.
    q = request.args.get("q")
    # Ensure that query is valid.
    if not q:
        raise RuntimeError("Please enter value for q parameter")
    # Search postal_code column for query value.
    pc_search_result = db.execute(
            "SELECT * from places WHERE postal_code LIKE :q", q=q+"%")
    # Check if we got some result set for postal_code search.
    if not pc_search_result:
        # If not, continue to search inside place+name, admin_name1 etc.
        name_search_result = db.execute(
                """SELECT * from places WHERE place_name LIKE :q
                """, q=q+"%")
        if not name_search_result:
            q = re.split("[,+]", q)
            for phrase in q:
                name_search_result = db.execute(
                    """SELECT * from places WHERE admin_name1 LIKE :q
                    OR admin_code1 LIKE :q
                    """, q=phrase+"%")
        if not name_search_result:
            # Return empty array if there's no match inside all checked columns.
            return jsonify([])
        else:
            # Return first 10 name result records.
            return jsonify(name_search_result[:10])
    else:
        # Return first 10 postal code result records.
        return jsonify(pc_search_result[:10])

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
