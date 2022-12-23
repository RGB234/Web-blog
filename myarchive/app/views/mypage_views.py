from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from ..models import User
from ..forms import UserLoginForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/<user_name>')
def homepage(user_name):
    page = request.args.get('page', type=int, default=1) 
    #GET요청방식 URL에서 'page'값을 가져옴 ex)localhost:5000/mypage/<username>/?page=5
    
    username = User.query.filter_by(username=user_name).first().username
    return render_template('homepage.html')

@bp.route('/posting')
def posting():
    return render_template('posting_form.html')