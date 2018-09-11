import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

from initdb import Rider, Station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///GoBike.sqlite"

db = SQLAlchemy(app)

# route for index.html - inital page
@app.route("/")
def home():
    return render_template("index.html")

@app.rout("/api/gobike")
def gobike():
    results = db.session.query(Station.station_id, 
                                Station.station_name, 
                                Station.latitutde, 
                                Station.longitude).all()
    return 0