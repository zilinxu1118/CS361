📦 Movie Info Microservice – README
(Implemented for Gavin Black by Zilin Xu)

🧾 Description
This microservice accepts a movie title and duration via a REST API and returns the watch time and a short description of the movie.

🤝 Communication Contract
Request Method: HTTP POST

Request URL: http://127.0.0.1:5000/movie-info

Request Format: JSON

Response Format: JSON

Communication Method: REST API (via requests library or similar)

Assumption: Microservice is running on localhost (127.0.0.1) and port 5000.

📤 How to REQUEST Data
Send an HTTP POST request to http://127.0.0.1:5000/movie-info
with a JSON payload containing:

Field	           Type	                  Description
title	          string	            Title of the movie
duration	         int	            Watch time in minutes

✅ Example Request (Python)
import requests

response = requests.post(
    "http://127.0.0.1:5000/movie-info",
    json={
        "title": "Finding Nemo",
        "duration": 100
    }
)

📥 How to RECEIVE Data
You will receive a JSON object with the following structure:

Field	              Type	              Description
title	            string	              Echoed title of the movie
watch_time	      string	              Watch time (e.g., "100 minutes")
description	      string	              Description of the movie

✅ Example Response (Python)

data = response.json()
print(data["title"])        # "Finding Nemo"
print(data["watch_time"])   # "100 minutes"
print(data["description"])  # "'Finding Nemo' is an entertaining movie that runs for 100 minutes."

UML Diagram
<img width="877" height="254" alt="image" src="https://github.com/user-attachments/assets/fea27025-f6a6-46d3-9c43-eefc4105cad7" />



