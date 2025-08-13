# Zilin Xu
# Package Tracking System -  microservice_c
# A microservice that exports package history

"""
GET /export_all?format=csv|json → All packages

GET /export_package/<id>?format=csv|json → One package
"""

from flask import Flask, request, jsonify, send_file
import os
import csv
import io

app = Flask(__name__)
DATA_FILE = "data.txt"

def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    data.append({
                        "id": parts[0],
                        "name": parts[1],
                        "address": parts[2],
                        "status": parts[3]
                    })
    return data

@app.route("/export_all", methods=["GET"])
def export_all():
    fmt = request.args.get("format", "csv").lower()
    data = load_data()

    if fmt == "json":
        return jsonify(data)
    elif fmt == "csv":
        output = io.StringIO()
        fieldnames = ["id", "name", "address", "status"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name="all_packages.csv"
        )
    else:
        return jsonify({"error": "Invalid format"}), 400

@app.route("/export_package/<package_id>", methods=["GET"])
def export_package(package_id):
    fmt = request.args.get("format", "csv").lower()
    data = load_data()
    package = next((p for p in data if p["id"] == package_id), None)

    if not package:
        return jsonify({"error": "Package not found"}), 404

    if fmt == "json":
        return jsonify(package)
    elif fmt == "csv":
        output = io.StringIO()
        fieldnames = ["id", "name", "address", "status"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(package)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"package_{package_id}.csv"
        )
    else:
        return jsonify({"error": "Invalid format"}), 400


if __name__ == "__main__":
    app.run(port=5002, debug=True)

