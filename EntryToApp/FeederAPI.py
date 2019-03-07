from datetime import datetime

import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)
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
        external_helper.insert_data_into_db(request_data)
        return "Done"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
