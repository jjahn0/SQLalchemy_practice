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

import pymysql
import pandas as pd
pymysql.install_as_MySQLdb()

Base = declarative_base()

from flask_sqlalchemy import SQLAlchemy

# from initdb import Rider, Station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///GoBike.sqlite"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Rider(db.Model):
    __tablename__ = 'rider'
    id = Column(db.Integer, primary_key=True)
    bike_id = Column(db.Integer, nullable=False)
    start_time = Column(db.Integer, nullable=False)
    start_station_id = Column(db.Integer)
    end_time = Column(db.Integer, nullable=False)
    end_station_id = Column(db.Integer)
    duration = Column(db.Integer, nullable=False)
    user_type = Column(db.Integer, nullable=True)
    member_age = Column(db.Integer, nullable=True)
    member_gender = Column(db.Integer, nullable=True)

class Station(db.Model):
    __tablename__ = 'station'
    id = Column(db.Integer, primary_key=True)
    station_id = Column(db.Integer, unique=True, nullable=False)
    station_name = Column(db.String(255), unique=True, nullable=False)
    latitude = Column(db.Float, nullable=False)
    longitude = Column(db.Float, nullable=False)
    neighborhood = Column(db.String(255))
    zipcode = Column(db.Integer)


# route for index.html - inital page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/gobike")
def gobike():
    result = []
    entry = {}
    test = {
        "id": 101,
        "name": "Happy Gilmore",
        "sport" : ["hockey","golf", "Fooseball"]
    }
    stationQuery = db.session.query(Station.station_id, 
                                Station.station_name, 
                                Station.latitude, 
                                Station.longitude).all()
    for _row in stationQuery:
        entry = {
            "station_id" : _row.station_id,
            "station_name" : _row.station_name,
            "latitude" : _row.latitude,
            "longitude" : _row.longitude
        }
        result.append(entry)

    # return jsonify(result)
    return jsonify(test)
        

if __name__ == "__main__":
    app.run(debug=True)
