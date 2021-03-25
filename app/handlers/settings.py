from flask import Blueprint, jsonify, request, abort
import logging

routes = Blueprint("settings", __name__, url_prefix="/api/settings")

