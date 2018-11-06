import datetime as dt 
import numpy as np 
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table

from flask import Flask, jsonify, render_template

## Database
engine = create_engine("sqlite:///GoBike.sqlite")

metadata = MetaData()
Stations = Table('station', metadata, autoload=True, autoload_with=engine)
Riders = Table('rider', metadata, autoload=True, autoload_with=engine)

session = Session(engine)

## Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List of available api routes."""
    return(
        f"Available Routes:<br/>"
        f"application program interface v.1 (riders) ... /api/v1.0/riders<br/>"
        f"application program interface v.2 (riders) ... /apt/v2.0/riders<br/>"
        f"application program interface (stations) ... /api/v1.0/stations<br><br>"
        f"rider data table  ...  /table"
    )

@app.route("/table")
def table():
    """displays rider data in a table format"""
    return render_template("table.html")


@app.route("/api/v1.0/stations")
def api_stations():
    """return a list of all station data"""
    #Query all stations
    results = session.query(Stations).all()

    #convert list of tuples into normal list
    all_station_data = list(np.ravel(results))

    return jsonify(all_station_data)


import pandas as pd


@app.route("/api/v2.0/stations")
def api2_stations():
    """return a list of referenced station data"""
    station_dictionary = pd.read_sql('SELECT * FROM station;', engine.connect()).to_dict(orient='records')

    return jsonify(station_dictionary)


@app.route("/api/v1.0/riders")
def api_riders():
    """return a list of rider data."""
    rider_results = session.query(Riders).all()
    all_rider_data = list(np.ravel(rider_results))

    return jsonify(all_rider_data)


@app.route("/api/v2.0/riders")
def api2_riders():
    """return referenced rider data"""
    rider_dict = pd.read_sql('SELECT * FROM rider;', engine.connect()).astype(float).to_dict(orient='records')
    return jsonify(rider_dict)


if __name__ == "__main__":
    app.run(debug=True)