from flask import Blueprint, jsonify, request, abort
import logging

from app import mpdservice

routes = Blueprint("playlists", __name__, url_prefix="/api/playlists")

@routes.route("", methods=['GET'])
def playlists_info_handler():
    # Получить список плейлистов или информацию об одном
    # из них
    playlistname = request.args.get('playlistname', None)
    data, code = mpdservice.get_playlist(playlistname)

    return jsonify(data), code

@routes.route("/play", methods=['GET'])
def switch_current_song_or_playlist_handler():
    # Переключить песню в текущем плейлисте
    songpos = request.args.get('songpos', None)
    playlistname = request.args.get('playlistname', None)
        
    # Если запрос без аргументов
    if not songpos or not playlistname:
        abort(400)

    if playlistname=="current" and not songpos:
        abort(400) 

    # Проверка на текущий плейлист
    if songpos and playlistname=="current":
        _, code = mpdservice.select_song_in_current_playlist(songpos)
    # Иначе загружаем сохраненный плейлист
    else:
        _, code = mpdservice.play_saved_playlist(playlistname, songpos)


    return jsonify(None), code    

@routes.route("", methods=['DELETE'])
def delete_song_or_playlist_handler():
    # Удаление трека из плейлиста
    songpos = request.args.get('songpos', None)
    playlistname = request.args.get('playlistname', None)

    if not playlistname:
        abort(400)

    if songpos:
        data, code = mpdservice.delete_song_in_playlist(playlistname, songpos)
    else:
        data, code = mpdservice.delete_playlist(playlistname)

    return jsonify(data), code
    
@routes.route("/save", methods=['POST'])
def save_curent_playlist_handler():
    # Список воспроизведение > плейлист
    try:
        req_data = request.get_json()
        playlistname = req_data['playlistname']
    except Exception as e:
        logging.error(e)
        abort(400)

    _, code = mpdservice.save_current_playlist(playlistname)

    return jsonify(None), code

@routes.route("/rename", methods=['POST'])
def rename_playlist_handler():
    # Переименовать плейлист
    try:
        req_data = request.get_json()
        current_name = req_data['currentname']
        new_name = req_data['newname']
    except Exception as e:
        logging.error(e)
        abort(400)

    _, code = mpdservice.rename_playlist(current_name, new_name)

    return jsonify(None), code

@routes.route("/swap", methods=['POST'])
def swap_songs_handler():
    # Поставить песню в другую позицию в плейлисте
    try:
        req_data = request.get_json()
        playlistname = req_data['playlistname']
        cur_pos = req_data['currentpos']
        new_pos = req_data['newpos']
    except Exception as e:
        logging.error(e)
        abort(400)

    data, code = mpdservice.swap_songs_in_playlist(playlistname, cur_pos, new_pos)

    return jsonify(data), code