from flask import Flask, request, render_template, request
from scraper import ATP
from twitter import Tweet
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
atp = ATP()
twitter = Tweet()


@app.route('/load_players', methods=["POST", "GET"])
def load_players():
    players = atp.get_players()
    for player in players:
        player['rating'] = twitter.get_rating(player['name'])
    return json.dumps({"success": True, "result": players})

@app.route('/get_player_rating', methods=["POST", "GET"])
def get_player_rating():
    pass
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)