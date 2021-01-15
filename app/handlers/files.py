from flask import Blueprint, jsonify, request, abort
import logging

from app import mpdservice

routes = Blueprint("files", __name__, url_prefix="/api/files")

@routes.route("", methods=['GET'])
def directory_info_handler():
    # Отправка содержимого доступных директорий
    path = request.args.get('path', None)
    data, code = mpdservice.get_directory(path)
    
    if code == 500:
        abort(500)

    return jsonify(data), code 

@routes.route("/update", methods=['GET'])
def update_db_handler():
    # Ручное обновление базы данных mpd
    _, code = mpdservice.update_mpd_database()
    if code == 500:
        abort(500)
    
    return jsonify(None), code

@routes.route("/add", methods=['POST'])
def add_path_to_playlist_handler():
    # Добавление файла или директории в текущий или сохраненный плейлисты
    try:
        req_data = request.get_json()
        path = req_data['path']
        playlistname = req_data['playlistname']
    except Exception as e:
        logging.error(e)
        abort(400)

    _, code = mpdservice.song_to_playlist(path, playlistname)

    if code == 500:
        abort(500)

    return jsonify(None), code

@routes.route("/play", methods=['POST'])
def play_path_handler():
    # Очистка списка воспроизведения и добавление
    # директории или файла 
    try:
        req_data = request.get_json()
        path = req_data['path']
    except Exception as e:
        logging.error(e)
        abort(400)

    _, code = mpdservice.clear_and_play(path)
    if code == 500:
        abort(500)

    return jsonify(None), code
