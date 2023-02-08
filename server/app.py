from flask import Flask, request, render_template, request
# from scrapers import tennis_scraper
from twitter import Tweet
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# atp = tennis_scraper()
twitter = Tweet()


# @app.route('/load_players', methods=["POST", "GET"])
# def load_players():
#     players = atp.get_players()
#     for player in players:
#         player['rating'] = twitter.calculate_player_rating(player['name'])
#     return json.dumps({"success": True, "result": players})

@app.route('/get_player_rating', methods=["POST", "GET"])
def get_player_rating():
    name = request.args.get('p').replace('%20', ' ')
    rating = twitter.calculate_player_rating(name)
    return json.dumps({"success": True, "result": rating})
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
