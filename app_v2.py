import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import pymysql
import pandas as pd
# pymysql.install_as_MySQLdb()

# Base = declarative_base()

# from flask_sqlalchemy import SQLAlchemy

# from initdb import Rider, Station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///GoBike.sqlite"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)
engine = create_engine("sqlite:///GoBike.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Rider = Base.classes.rider

session = Session(engine)

# route for index.html - inital page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/v1.0/stations")
def stations():
    station_all = []
    station_one = {}
    test = {
        "id": 101,
        "name": "Happy Gilmore",
        "sport" : ["hockey","golf", "Fooseball"]
    }
    result = session.query(Station).all()

    for _row in result:
        station_one = {
            "station_id" : _row.station_id,
            "station_name" : _row.station_name,
            "latitude" : _row.latitude,
            "longitude" : _row.longitude
        }
        station_all.append(station_one)

    # return jsonify(result)
    return jsonify(test)
        

if __name__ == "__main__":
    app.run(debug=True)
