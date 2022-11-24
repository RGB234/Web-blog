from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..forms import UserLoginForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/<str:username>/')
def homepage():
    return None