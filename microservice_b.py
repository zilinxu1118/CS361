# Zilin Xu
# Package Tracking System - microservice_b
# A microservice that saves and loads package data

"""
POST /save_package → Saves package to packages.json

GET /load_package/<id> → Loads specific package
"""

from flask import Flask, jsonify, request
import os

app = Flask(__name__)
DATA_FILE = "data.txt"

# ---------------------------
# Helper Functions
# ---------------------------

def load_packages():
    packages = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    packages.append({
                        "id": parts[0],
                        "name": parts[1],
                        "address": parts[2],
                        "status": parts[3]
                    })
    return packages

def save_packages(packages):
    with open(DATA_FILE, "w") as f:
        for p in packages:
            f.write(f"{p['id']},{p['name']},{p['address']},{p['status']}\n")

# ---------------------------
# Routes
# ---------------------------

@app.route("/save_package", methods=["POST"])
def save_package():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No package data provided"}), 400

    packages = load_packages()
    packages.append(data)
    save_packages(packages)
    return jsonify({"message": "Package saved successfully"}), 200

@app.route("/save_all_packages", methods=["POST"])
def save_all_packages():
    """Overwrite entire package storage (used to remove drafts)"""
    data = request.get_json()
    if not data or "packages" not in data:
        return jsonify({"error": "No packages provided"}), 400

    save_packages(data["packages"])
    return jsonify({"message": "All packages saved successfully"}), 200

@app.route("/export_history", methods=["GET"])
def export_history():
    packages = load_packages()
    return jsonify({"packages": packages}), 200

@app.route("/load_package/<pkg_id>", methods=["GET"])
def load_package(pkg_id):
    packages = load_packages()
    package = next((p for p in packages if p["id"] == pkg_id), None)
    if not package:
        return jsonify({"error": "Package not found"}), 404
    return jsonify({"package": package}), 200

@app.route("/delete_package/<pkg_id>", methods=["DELETE"])
def delete_package(pkg_id):
    packages = load_packages()
    new_packages = [p for p in packages if p["id"] != pkg_id]

    if len(new_packages) == len(packages):
        return jsonify({"error": "Package not found"}), 404

    save_packages(new_packages)
    return jsonify({"message": f"Package {pkg_id} deleted successfully"}), 200

@app.route("/update_package_status/<pkg_id>", methods=["PUT"])
def update_package_status(pkg_id):
    data = request.get_json()
    new_status = data.get("status", "").strip()
    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    packages = load_packages()
    found = False
    for p in packages:
        if p["id"] == pkg_id:
            p["status"] = new_status
            found = True
            break

    if not found:
        return jsonify({"error": "Package not found"}), 404

    save_packages(packages)
    return jsonify({"message": f"Status for package {pkg_id} updated to '{new_status}'"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
