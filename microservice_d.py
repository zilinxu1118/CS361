# Zilin Xu
# Package Tracking System -  microservice_d
# A microservice that estimates shipping time
"""
POST /estimate → Calculate delivery time from distance + shipping type

"""

from flask import Flask, request, jsonify
from time import time

app = Flask(__name__)

SHIPPING_SPEEDS = {
    "express": 800,  # km/day
    "standard": 400
}

@app.route("/estimate", methods=["POST"])
def estimate():
    start_time = time()
    data = request.get_json()
    if not data or "distance" not in data or "shipping_type" not in data:
        return jsonify({"error": "Invalid input. Provide 'distance' and 'shipping_type'."}), 400

    try:
        distance = float(data["distance"])
        shipping_type = data["shipping_type"].strip().lower()

        if shipping_type not in SHIPPING_SPEEDS:
            return jsonify({"error": f"Invalid shipping type. Choose from {list(SHIPPING_SPEEDS.keys())}"}), 400

        days = round(distance / SHIPPING_SPEEDS[shipping_type], 2)
        elapsed = time() - start_time
        return jsonify({"estimated_days": days, "elapsed": elapsed}), 200
    except ValueError:
        return jsonify({"error": "Distance must be a number."}), 400


if __name__ == "__main__":
    app.run(port=5003, debug=True)
