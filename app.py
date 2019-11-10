import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Flask Setup
#################
app = Flask(__name__)

######
# Database Setup
##########
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Routes
###############

@app.route("/")
def welcome():
    """Welcome to the Hawaii Climate information Site."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    oneyear_pcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    session.close()

    # Dict with date as the key and prcp as the value
    precipitation_yr = {date: prcp for date, prcp in oneyear_pcp}
    return jsonify(precipitation_yr)

@app.route("/api/v1.0/stations")
def station_list():
    session = Session(engine)

    """Return a list of stations."""
    list_stn = session.query(Station.station).all()
    
    # Unravel results into a 1D array and convert to a list
    stations_list = list(np.ravel(list_stn))
    return jsonify(stations_list)

    session.close()

@app.route("/api/v1.0/tobs")
def temp_monthly():
     session = Session(engine) 
     # Calculate the date 1 year ago from last date in database
     query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
     # Query the primary station for all tobs from the last year
     results = session.query(Measurement.tobs).\
         filter(Measurement.station == 'USC00519281').\
         filter(Measurement.date >= query_date).all()

     # Unravel results into a 1D array and convert to a list
     temp_oneyr = list(np.ravel(results))

     # Return the results
     return jsonify(temp_oneyr)   

     session.close()

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def cal_temp(start=None, end=None):
     session = Session(engine) 
     cal  = [func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
     if not end:
        #calcuate averages for start
        calcuation = session.query(*cal).\
            filter(Measurement.date >= start).all()
        #unravel into array and put into list.
        averages =  list(np.ravel(calcuation))
        return jsonify(averages)
    
    #calcuate averages for start and end
     calcuation = session.query(*cal).\
        filter(Measurement.date >= start).all().\
        filter(Measurement.date <= end).all()
    
    #unravel into array and put into list.
     averages =  list(np.ravel(calcuation))
     return jsonify(averages)

     session.close()

if __name__ == '__main__':
    app.run(debug=True)

