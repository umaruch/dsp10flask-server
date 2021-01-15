from flask import Flask
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
