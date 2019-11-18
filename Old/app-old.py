import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
########
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
#########
app = Flask(__name__)

# Flask Routes
########
@app.route("/")
def welcome():
    """Welcome to the Hawaii Climate information Site."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    oneyear_pcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    # Dict with date as the key and prcp as the value
    precp_one = {date: prcp for date, prcp in oneyear_pcp}
    return jsonify(precp_one)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    station_list = session.query(Station.station).all()

    # Unravel results into a 1D array and convert to a list
    stations_flat = list(np.ravel(results))
    return jsonify(stations_flat)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    oneyear_temp = session.query(Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()

    # Unravel results into a 1D array and convert to a list
    temp_flat = list(np.ravel(oneyear_temp))

    # Return the results
    return jsonify(temps)