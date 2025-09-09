from flask import Blueprint

bp = Blueprint('blueprints', __name__)

from . import auth, dashboard, api, guild