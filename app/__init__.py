from flask import Flask, make_response, jsonify
import logging

import config

app = Flask(__name__)

logging.basicConfig(
    filename=config.LOG_FILE,
    filemode="a",
    format='%(asctime)s [%(levelname)s]: %(message)s',
    level=logging.DEBUG
)

from .handlers import player, playlists, files
app.register_blueprint(player.routes)
app.register_blueprint(playlists.routes)
app.register_blueprint(files.routes)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def error_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(500)
def server_exception(error):
    return make_response(jsonify({'error': 'Server error'}), 500)