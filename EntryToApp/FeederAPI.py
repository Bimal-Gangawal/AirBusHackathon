from datetime import datetime

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from ExternalHelper.ExternalHelper import ExternalHelperMethods

external_helper = ExternalHelperMethods()


@app.route('/HeathCheck', methods=['GET'])
def api_health_check():
    try:
        response = {'Status': True, "TimeStamp": datetime.now()}
        return jsonify(response)
    except Exception as e:
        response = {'Status': False, "TimeStamp": datetime.now(), "Message": e}
        return jsonify(response)


@app.route('/FlightsData', methods=['POST'])
def post_data_in_db():
    columns = ["MSN", "HarnessLength", "FlightProgram", "GrossWeight", "AtmPressure", "RoomTemp",
               "Airport", "FuelCapacityLeft", "FuelCapacityRight", "FuelQuantityRight",
               "FuelQuantityLeft", "MaxAltitude", "FlightNo"]
    if not request.json and not sorted(list(request.json.keys())) == sorted(columns) in request.json:
        return jsonify({"Status": False, "Message": "Improper JSON Body"})
    else:
        request_data = pd.DataFrame(pd.Series(request.json)).T
        status = external_helper.insert_data_into_db(request_data)
        if status:
            return "Done"
        else:
            return "Update fail"


@app.route('/getFilterFlightData', methods=['GET', 'POST'])
def getFilteredData():

    columns = ["MSN", "HarnessLength", "FlightProgram", "GrossWeight", "AtmPressure", "RoomTemp",
               "Airport", "FuelCapacityLeft", "FuelCapacityRight", "FuelQuantityRight",
               "FuelQuantityLeft", "MaxAltitude", "FlightNo"]
    if request.method == "POST":
        if not request.json and not set(columns).issubset(set(list(request.json.keys()))):
            return jsonify({"Status": False, "Message": "Improper JSON Body"})
    else:
        flights_info = external_helper.get_my_sql_data()
        if 'MSN' in request.args:
            msn = request.args.get('MSN')
            flights_info = flights_info[flights_info['MSN'] == int(msn)]
        if 'HarnessLength' in request.args:
            harnesslength = request.args.get('HarnessLength')
            flights_info = flights_info[flights_info['HarnessLength'] == int(harnesslength)]
        if 'FlightProgram' in request.args:
            FlightProgram = request.args.get('FlightProgram')
            flights_info = flights_info[flights_info['FlightProgram'] == FlightProgram]
        if 'AtmPressure' in request.args:
            AtmPressure = request.args.get('AtmPressure')
            flights_info = flights_info[flights_info['AtmPressure'] == int(AtmPressure)]
        if 'RoomTemp' in request.args:
            RoomTemp = request.args.get('RoomTemp')
            flights_info = flights_info[flights_info['RoomTemp'] == int(RoomTemp)]
        if 'Airport' in request.args:
            Airport = request.args.get('Airport')
            flights_info = flights_info[flights_info['Airport'] == Airport]
        if 'FuelCapacityLeft' in request.args:
            FuelCapacityLeft = request.args.get('FuelCapacityLeft')
            flights_info = flights_info[flights_info['FuelCapacityLeft'] == int(FuelCapacityLeft)]
        if 'FuelCapacityRight' in request.args:
            FuelCapacityRight = request.args.get('FuelCapacityRight')
            flights_info = flights_info[flights_info['FuelCapacityRight'] == int(FuelCapacityRight)]
        if 'FuelQuantityRight' in request.args:
            FuelQuantityRight = request.args.get('FuelQuantityRight')
            flights_info = flights_info[flights_info['FuelQuantityRight'] == int(FuelQuantityRight)]
        if 'FuelQuantityLeft' in request.args:
            FuelQuantityLeft = request.args.get('FuelQuantityLeft')
            flights_info = flights_info[flights_info['FuelQuantityLeft'] == int(FuelQuantityLeft)]
        if 'MaxAltitude' in request.args:
            MaxAltitude = request.args.get('MaxAltitude')
            flights_info = flights_info[flights_info['MaxAltitude'] == int(MaxAltitude)]
        if 'FlightNo' in request.args:
            FlightNo = request.args.get('FlightNo')
            flights_info = flights_info[flights_info['FlightNo'] == FlightNo]
        result = '''
        <html>
        <head>
        <style>

            h2 {
                text-align: center;
                font-family: Helvetica, Arial, sans-serif;
            }
            table { 
                margin-left: auto;
                margin-right: auto;
            }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: center;
                font-family: Helvetica, Arial, sans-serif;
                font-size: 90%;
            }
            table tbody tr:hover {
                background-color: #dddddd;
            }
            .wide {
                width: 90%; 
            }

        </style>
        </head>
        <body>
            '''
        result += flights_info.to_html(classes='wide', escape=False,index=False)
        result += '''
        </body>
        </html>
        '''
        return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
