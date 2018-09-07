import pandas as pd
from flask import Flask, jsonify
import datetime as dt
import time
from data import wiki_fire_df

#Designning a Flask API based on the queries that you have just developed
app = Flask(__name__)


# Flask Routes 
#"""List all available api routes."""
@app.route("/routes") 
def routes():
    return ( 
         f"<h3>Routes:</h3></br>"
         f"- Full list of fires: /api/v1.0/wild-fires/<br/>" 
         f"- List of fires by year: /api/v1.0/wild-fires/<year><br/>"
         f"- List of fires greater from year provided to date: /api/v1.0/wildfires/greaterthan/<year><br/>"
        #  f"/api/v1.0/start<br/>" 
        #  f"- With start date, come out the MAX, MIN and AVG temperature for all dates from that date of last year  to greater than and equal to that date<br/>" 
        #  f"/api/v1.0/start/end<br/>" 
        #  f"- With start date and the end date, come out the MAX, MIN and AVG temperature in between of those dates<br/>" 
           ) 

@app.route("/api/v1.0/wildfires/")
def wildfires():
    data = wiki_fire_df[["Fire Year","Fire Name","County","Acres Burned"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)

@app.route("/api/v1.0/wildfires/<year>")
def wildfiresbyyear(year):
    data = wiki_fire_df.loc[wiki_fire_df["Fire Year"] == int(year),["Fire Year","Fire Name","County","Acres Burned"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)

@app.route("/api/v1.0/wildfires/greaterthan/<year>")
def wildfiresgreaterthanyear(year):
    data = wiki_fire_df.loc[wiki_fire_df["Fire Year"] >= int(year),["Fire Year","Fire Name","County","Acres Burned","Number of Days"]]

    formatted_data = data.to_dict('records')
    return jsonify(formatted_data)

# @app.route("/api/v1.0/tobs")
# def tobs():
#     max_date_str = engine.execute("SELECT MAX(date) AS date FROM measurements").fetchall()
#     max_date = pd.to_datetime(max_date_str[0][0])
#     start_date = max_date - dt.timedelta(days=365)
#     year_data = pd.read_sql_query(f"SELECT date,tobs FROM measurements WHERE date >= '{start_date}' AND date <= '{max_date}' ORDER BY date", session.bind)
    
#     formatted_data = year_data.to_dict('records')
#     return jsonify(formatted_data)

# @app.route("/api/v1.0/from/<start_date>")
# def start(start_date):    
#     temp_data = engine.execute(f"SELECT MIN(tobs),MAX(tobs),AVG(tobs) FROM measurements WHERE date >= '{start_date}'").fetchall()
#     temp_dict = {"Min":temp_data[0][0],"Max":temp_data[0][1],"Avg":round(temp_data[0][2],2)}
#     return jsonify(temp_dict)

# @app.route("/api/v1.0/fromto/<start_date>/<end_date>")
# def startend(start_date,end_date):
#     temp_data = engine.execute(f"SELECT MIN(tobs),MAX(tobs),AVG(tobs) FROM measurements WHERE date >= '{start_date}' AND date <= '{end_date}'").fetchall()
#     temp_dict = {"Min":temp_data[0][0],"Max":temp_data[0][1],"Avg":round(temp_data[0][2],2)}
#     return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)