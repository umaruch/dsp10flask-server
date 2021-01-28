import mpd
import logging

import config

client = mpd.MPDClient()

def connection(func):
    # Переподключение в случае отвала соединения с плеером
    def wrapper(*args):
        try:
            return func(*args)
        except mpd.base.ConnectionError:
            try:
                client.connect(config.MPD_HOST, config.MPD_PORT)
                return func(*args)
            except mpd.base.ConnectionError:
                logging.error("Connection to MPD error")
                return None, 500
        except mpd.base.CommandError as e:
            logging.exception("message")
            return None, 500
    return wrapper

###### Функции проигрывателя

# Отправка текущего статуса и трека
@connection
def status(value):
    status = client.status()
    status['songinfo'] = client.currentsong()
    return status, 200    

# Переключение на проигрывание
@connection
def play(value):
    client.play()
    return None, 204

# Переключение на паузу
@connection
def pause(value):
    client.pause()
    return None, 204

# Остановка воспроизведения
@connection
def stop(value):
    client.stop()
    return None, 204

# Переключение на другой временной промежуток
@connection
def to_time(value):
    client.seekcur(value)
    return None, 204

# Следующий трек
@connection
def next(value):
    try:
        client.next()
    except mpd.base.CommandError:
        client.play(0)
    return None, 204

# Предыдущий трек
@connection
def prev(value):
    try:
        client.previous()
    except:
        client.play(0)
    return None, 204

# Изменение громкости
@connection
def volume(value):
    client.setvol(value)
    return None, 204


# Переключение режимов повтора
@connection
def repeat(value):
    if value == 0:
        client.repeat(0)
        client.single(0)
    if value == 1:
        client.repeat(1)
        client.single(0)
    if value == 2:
        client.repeat(1)
        client.single(1)
    return None, 204

# Переключение рандомного воспроизведения
@connection
def random(value):
    client.random(value)
    return None, 204

###### Функии плейлистов

# Получение списка плейлистов или информации о конкретном
@connection
def get_playlist(name):
    try:
        if not name:
            return client.listplaylists(), 200
        if name == "current":
            return client.playlistinfo(), 200
        else:
            return client.listplaylistinfo(name), 200
    except mpd.base.CommandError as e:
        logging.error(e)
        return {'error': 'No such playlist'}, 404

# Сменить трек в текущем плейлисте
@connection
def select_song_in_current_playlist(songpos):
    try:
        client.play(songpos)
        return None, 204
    except mpd.base.CommandError:
        return {'error':'No such song position'}, 404

# Поменять позицию трека в плейлисте
@connection
def swap_songs_in_playlist(playlistname, pos1, pos2):
    try:
        if playlistname == "current":
            client.swap(pos1, pos2)
            return client.playlistinfo(), 200
        else:
            client.playlistmove(playlistname, pos1, pos2)
            return client.listplaylistinfo(playlistname), 200
    except mpd.base.CommandError:
        return {'error':'No such song position or playlist'}, 404

# Удалить трек из плейлиста
@connection
def delete_song_in_playlist(playlistname, songpos):
    try:
        if playlistname == "current":
            client.delete(songpos)
            return client.playlistinfo(), 200
        else:
            client.playlistdelete(playlistname, songpos)
            return client.listplaylistinfo(playlistname), 200
    except mpd.base.CommandError:
        return {'error':'No such song position or playlist'}, 404

# Сохранить текущий список воспроизведения в плейлист
@connection
def save_current_playlist(playlistname):
    client.save(playlistname)
    return None, 204
        
# Переименовить сохраненный плейлист
@connection
def rename_playlist(origin_name, new_name):
    try:
        client.rename(origin_name, new_name)
        return None, 204
    except mpd.base.CommandError:
        return {'error':'No such playlist'}, 404

# Удалить сохраненный плейлист
@connection
def delete_playlist(playlistname):
    try:
        if playlistname == "current":
            client.clear()
            return {}, 200

        client.rm(playlistname)
        return client.listplaylists(), 200
    except mpd.base.CommandError:
        return {'error':'No such playlist'}, 404

# Воспроизводить сохраненный плейлист
@connection
def play_saved_playlist(playlistname, songpos):
    try:
        client.clear()
        client.load(playlistname)
        if not songpos:
            client.play()
        else:
            client.play(songpos)
            
        return None, 204
    except mpd.base.CommandError:
        return {'error':'No such playlist'}, 404

###### Функции работы с файлами

# Получить файлы в директории
@connection
def get_directory(directory):
    try:
        if directory:
            return client.lsinfo(directory), 200
        else:
            return client.lsinfo(), 200
    except mpd.base.CommandError:
        return {'error':'No such directory'}, 404

# Обновить базу данных MPD
@connection
def update_mpd_database():
    client.update()
    return client.lsinfo(), 200

# Добавить трек в один из плейлистов
@connection
def song_to_playlist(uri, playlistname):
    try:
        if playlistname == "current":
            client.add(uri)
        else:
            client.playlistadd(playlistname, uri)
        return None, 204
    except mpd.base.CommandError:
        return {'error':'No such playlist of song/dir'}, 404

# Воспроизвести трек или папку
@connection
def clear_and_play(uri):
    try:
        client.clear()
        client.add(uri)
        client.play()
        return None, 204
    except mpd.base.CommandError:
        return {'error':'No such song/dir'}, 404


