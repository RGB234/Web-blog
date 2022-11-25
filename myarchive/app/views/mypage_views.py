from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..models import User
from ..forms import UserLoginForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/<username>/')
def homepage(user_id):
    username = User.query.filter_by(id=user_id).first().username
    return None