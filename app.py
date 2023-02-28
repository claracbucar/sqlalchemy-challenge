from flask import Flask
import sqlalchemy
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """Lists all available api routes"""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/names<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieves the last 12 months of precipitation data"""
    yearago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    dateandprcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= yearago).all()

    return jsonify(dateandprcp)


@app.route("/api/v1.0/stations")
def stations():
    """Returns a JSON list of stations from the dataset."""
    totalstationsnames = session.query(Station)
    for stationname in totalstationsnames:
        print(stationname.station)
    return jsonify(totalstationsnames)

@app.route("/api/v1.0/tobs")
def temperatures():
    """Returns a JSON list of temperature observations for the previous year"""
    activestationlastyear = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= yearago).all()
    print(activestationlastyear)
    return jsonify(activestationlastyear)


session.close()


if __name__ == '__main__':
    app.run(debug=True)