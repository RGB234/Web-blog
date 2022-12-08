from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..models import User
from ..forms import UserLoginForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/<user_name>/')
def homepage(user_name):
    username = User.query.filter_by(username=user_name).first().username
    return render_template('homepage.html')