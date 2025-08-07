# Zilin Xu
# xuzili@oregonstate.edu
# 8/5/2025
# CS 361 Software Engineering 1
# Movie Information Microservice for Gavin Black
# This microservice provides movie information based on title and duration.
# It returns a description of the movie along with its watch time.


from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined movie descriptions (case-insensitive) (you should replace these with real data)
MOVIE_DESCRIPTIONS = {
    "Inception": "A mind-bending thriller by Christopher Nolan.",
    "The Matrix": "A sci-fi classic about reality and simulation.",
    "Finding Nemo": "A heartwarming Pixar film about a clownfish searching for his son.",
    "Interstellar": "A journey through space and time in search of a new home for humanity.",
    "The Lion King": "A Disney classic about courage, leadership, and the circle of life."
}

@app.route('/movie-info', methods=['POST'])
def movie_info():
    data = request.get_json()

    # Get input values
    title = data.get('title', 'Unknown Title').strip()
    duration = data.get('duration', 0)

    # Look up the movie description (case-insensitive)
    description = None
    for known_title in MOVIE_DESCRIPTIONS:
        if known_title.lower() == title.lower():
            description = MOVIE_DESCRIPTIONS[known_title]
            break

    if description is None:
        description = f"'{title}' is an entertaining movie."

    response = {
        "title": title,
        "watch_time": f"{duration} minutes",
        "description": description
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
