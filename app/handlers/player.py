from flask import Blueprint, jsonify, request, abort
import logging

from app import mpdservice

routes = Blueprint("player", __name__, url_prefix="/api/player")

# словарь команд и соотносящихся функций
commands = {
    'status': mpdservice.status,
    'play': mpdservice.play,
    'pause': mpdservice.pause,
    'stop': mpdservice.stop,
    'next': mpdservice.next,
    'prev': mpdservice.prev,
    'volume': mpdservice.volume,
    'repeat': mpdservice.repeat,
    'random': mpdservice.random,
    'time': mpdservice.to_time
}

@routes.route('', methods = ['GET'])
def run_command_handler():
    # получение команды от пользователя и ее обработка
    cmd = request.args.get('cmd', None)
    value = None
    # Проверка наличия в строке запроса команды
    if not cmd:
        abort(400)
    # Проверка на наличие и правильность доп. аргумента
    # там где надо 
    if cmd in ('volume', 'repeat', 'random', 'time'):
        try:
            value = int(request.args['value'])
        except Exception as e:
            logging.error(e)
            abort(400)
    try: 
        data, code = commands[cmd](value)
        print(data, code)
    except KeyError:
        abort(400)

    if code==500:
        abort(500)

    return jsonify(data), code
