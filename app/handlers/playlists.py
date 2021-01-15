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

    if code == 500:
        abort(500)

    return jsonify(data), code

@routes.route("/play")
def switch_current_song_handler():
    # Переключить песню в текущем плейлисте
    songpos = request.args.get('songpos', None)
    playlistname = request.args.get('playlistname', None)

    if songpos and playlistname:
        abort(400)
    
    if not songpos and not playlistname:
        abort(400)

    if songpos:
        _, code = mpdservice.select_song_in_current_playlist(songpos)
    if playlistname:
        _, code = mpdservice.play_saved_playlist(playlistname)

    if code == 500:
        abort(500)

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

    if code == 500:
        abort(500)

    return jsonify(data), code
    
@routes.route("/save", methods=['POST'])
def save_curent_playlist_handler():
    # Список воспроизведение > плейлист
    pass

@routes.route("/rename", methods=['POST'])
def rename_playlist_handler():
    # Переименовать плейлист
    pass

@routes.route("/swap", methods=['POST'])
def swap_songs_handler():
    # Поставить песню в другую позицию в плейлисте
    pass