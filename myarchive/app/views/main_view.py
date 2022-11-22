from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..forms import UserLoginForm

bp = Blueprint('main', __name__, url_prefix='/main')

def _homepage(id, pw):