from datetime import datetime
from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.utils import redirect

from app import db
from ..models import User, Post
from ..forms import PostingForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/<user_name>')
def homepage(user_name):
    page = request.args.get('page', type=int, default=1) #URL 에 page 값이 없으면 자동으로 1 적용
    #GET요청방식 URL에서 'page'값을 가져옴 ex)localhost:5000/mypage/<username>/?page=5
    
    posting_list = Post.query.filter_by(user_id=g.user.id).order_by(Post.create_date.desc())

    posting_list = posting_list.paginate(page = page, per_page=10) #posting_list 는 단순 Post 모델이 아니라 Pagination 객체가 된다
    username = User.query.filter_by(username=user_name).first().username
    return render_template('homepage.html', posting_list=posting_list)

@bp.route('/posting', methods=('GET', 'POST'))
def posting():
    form = PostingForm()

    if request.method == "POST" and form.validate_on_submit():
        post = Post(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), modify_date=datetime.now(), user=g.user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('mypage.homepage', user_name=g.user.username)) #g.user = User.query.get(user_id), user_id = user.id (login_views.py)

    return render_template('posting_form.html', form=form)