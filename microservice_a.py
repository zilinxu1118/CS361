# Adam Danielson
# danieada@oregonstate.edu
# 8/4/2025
# CS 361 Software Engineering 1
# Package ID Generator Microservice
# Microservice that generates a package ID following the format "PKG-[Year][Month][Day]-[Counter]"
# Additionally, the microservice can check that a specific ID is unique


from flask import Flask, request, jsonify
from datetime import datetime
from threading import Lock

app = Flask(__name__)

# Storage of issued IDs and a counter
issued_ids = set()
id_counter = {}
lock = Lock()


def generate_new_id():
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"PKG-{today}"

    with lock:
        if today not in id_counter:
            id_counter[today] = 1
        else:
            id_counter[today] += 1
    
        suffix = f"{id_counter[today]:03d}"
        new_id = f"{prefix}-{suffix}"
        issued_ids.add(new_id)
    return new_id


@app.route('/generate_id', methods = ['GET'])
def generate_id():
    new_id = generate_new_id()
    return jsonify({"id": new_id}), 200


@app.route('/check_id', methods = ['POST'])
def check_id():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({"error": "Missing 'id' in request"}), 400
    
    id_to_check = data['id']
    used = id_to_check in issued_ids
    return jsonify({"used": used}), 200


if __name__ == '__main__':
    app.run(debug = True, port = 5000)