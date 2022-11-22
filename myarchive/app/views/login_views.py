from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..forms import UserLoginForm

bp = Blueprint('login', __name__, url_prefix='/')

@bp.route('/')
def _login():
    return render_template('login.html')

    