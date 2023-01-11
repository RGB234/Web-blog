import re

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
    
    post_list = Post.query.filter_by(user_id=g.user.id).order_by(Post.create_date.desc())

    post_list = post_list.paginate(page = page, per_page=10) #post_list 는 단순 Post 모델이 아니라 Pagination 객체가 된다
    username = User.query.filter_by(username=user_name).first().username
    return render_template('homepage.html', post_list=post_list)

@bp.route('/post_write', methods=('GET', 'POST'))
def post_write():
    form = PostingForm()

    if request.method == "POST" and form.validate_on_submit():
        content_data = form.content.data
        content_data = re.sub('&nbsp;', '\t', content_data) #공백
        content_data = re.sub('</p>', '\n', content_data) #줄바꿈
        content_data = re.sub('</h[0-9]>', '\n', content_data) #줄바꿈
        content_data = re.sub('</code>', '\n', content_data) #코드블록 끝나면 줄바꿈
        content_data = re.sub('(<([^>]+)>)','', content_data); # 정규식(re) 사용하여 html 태그 제거
        post = Post(subject=form.subject.data, content=content_data, create_date=datetime.now(), modify_date=datetime.now(), user=g.user)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('mypage.homepage', user_name=g.user.username)) #g.user = User.query.get(user_id), user_id = user.id (login_views.py)

    return render_template('post_form.html', form=form)

@bp.route('/post_view/<int:post_id>')
def post_view(post_id):
    post = Post.query.filter_by(id=post_id)

    return render_template('post_view.html', post=post)