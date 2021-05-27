import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    """List all routes that are available"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )



@app.route("/api/vi.0/precipitation")
def precipitation():
    
    session = Session(engine)
    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > "2016-08-23").\
        all()

    session.close()

    all_precip = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp

        all_precip.append(precip_dict)

    return jsonify(all_precip)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    sta = session.query(station.station).\
            order_by(station.station).all()

    session.close()

    all_stations = list(np.ravel(sta))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)

    temp = session.query(measurement.date, measurement.tobs).\
            filter(measurement.date > "2016-08-23").\
            filter(measurement.station== "USC00519281").\
            order_by(measurement.date).all()

    session.close()

    all_temps = []
    for date, tobs in temp:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs

        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start(start_date):
    session = Session(engine)

    st_date = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()

    session.close()

    start_temp = []
    for min, avg, max in st_date:
        start_temp_dict = {}
        start_temp_dict['tmin'] = min
        start_temp_dict['tavg'] = avg
        start_temp_dict['tmax'] = max
        start_temp.append(start_temp_dict)

    return jsonify(start_temp)


@app.route("/api/v1.0/<start>")
def start_end(start_date, end_date):
    session = Session(engine)


    st_end_date = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()


    session.close()


    start_end_temp = []
    for min, avg, max in st_end_date:
        start_end_dict = {}
        start_end_dict['tmin'] = min
        start_end_dict['tavg'] = avg
        start_end_dict['tmax'] = max
        start_end_temp.append(start_end_dict)

    return jsonify(start_end_temp)



if __name__ == "__main__":
    app.run(debug=True)
