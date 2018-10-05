import datetime as dt 
import numpy as np 
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## Database
engine = create_engine("sqlite:///GoBike.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station

session = Session(engine)

## Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List of available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/riders<br/>"
        f"/api/v1.0/stations"
    )

@app.route("/api/v1.0/stations")
def stations():
    """return a list of all station names"""
    #Query all stations
    results = session.query(Station).all()

    #convert list of tuples into normal list
    all_station_names = list(np.ravel(results))

    return jsonify(all_station_names)

# @app.route("/api/v1.0/riders")
# def riders():
#     """return a list of rider data."""

if __name__ == "__main__":
    app.run(debug=True)