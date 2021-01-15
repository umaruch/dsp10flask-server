from flask import make_response, jsonify
from app import app

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def error_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(500)
def server_exception(error):
    return make_response(jsonify({'error': 'Server error'}), 500)