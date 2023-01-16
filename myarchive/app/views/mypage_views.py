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

    for post in post_list.items:
        # post.content = re.sub('</p>', '\n', post.content) #줄바꿈
        # post.content = re.sub('</h[0-9]>', '\n', post.content) #줄바꿈
        # post.content = re.sub('</code>', '\n', post.content) #코드블록 끝나면 줄바꿈
        post.content = re.sub('</[^>]*>', ' ', post.content) #html 태그 닫을 시 공백
        post.content = re.sub('(<([^>]+)>)','', post.content); # 정규식(re) 사용하여 html 태그 제거

        post.content = re.sub("&lt;", "<", post.content) 
        post.content = re.sub("&gt;", ">", post.content)
        post.content = re.sub("&amp;", "&", post.content)
        post.content = re.sub('&nbsp;', '\t', post.content) #공백

    username = User.query.filter_by(username=user_name).first().username
    return render_template('homepage.html', post_list=post_list)

@bp.route('/post_write', methods=('GET', 'POST'))
def post_write():
    form = PostingForm()

    if request.method == "POST" and form.validate_on_submit():
        post = Post(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), modify_date=datetime.now(), user=g.user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('mypage.homepage', user_name=g.user.username)) #g.user = User.query.get(user_id), user_id = user.id (login_views.py)
    #GET 형식 요청방식일 때(request.method == "GET")
    return render_template('post_form.html', form=form)

@bp.route('/post_view/<int:post_id>')
def post_view(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post_view.html', post=post)

@bp.route('/post_revision/<int:post_id>', methods=('GET', 'POST'))
def post_revision(post_id):

    post = Post.query.filter_by(id=post_id).first()
    form = PostingForm()

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(post) #populate_obj를 통해 form 에 저장된 데이터를 post에 적용
        post.modify_date = datetime.now()
        db.session.commit()
        return redirect(url_for('mypage.post_view', post_id=post.id)) #g.user = User.query.get(user_id), user_id = user.id (login_views.py)

    return render_template('post_revision.html', form=form, post=post) 

@bp.route('/delete/<int:post_id>')
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('mypage.homepage', user_name=g.user.username))