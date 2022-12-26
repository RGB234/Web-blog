from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from ..forms import UserLoginForm, UserCreateForm
from ..models import User

bp = Blueprint('login', __name__, url_prefix='')

@bp.route('/', methods=('GET', 'POST'))
def _login():
    
    ''' login.html 렌더링(request.method == 'GET') '''
    ''' 로그인 양식(UserLoginform)을 적절하게 채워서 제출(request.method == 'Post')하면 mypage.homepage호출'''
    ''' 어떤 경우에 GET / POST 요청이 들어오는지는 login.html에 구현'''

    form = UserLoginForm()
    #request는 flask에서 자동제공 참고:https://velog.io/@sangmin7648/%EC%98%A4%EB%8A%98%EC%9D%98-%EB%B0%B0%EC%9B%80-045
    if request.method == 'POST' and form.validate_on_submit(): #UserLoginForm()을 채운 뒤 로그인버튼을 누르면
        error = None
        user = User.query.filter_by(userid=form.userid.data).first() #검색
        if not user:
            error = "해당 사용자 계정이 존재하지 않습니다"
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 일치하지 않습니다"
        
        if error is None: #제출된 UserLoginForm이 적절하다면 로그인
            session.clear()
            '''flask session에 key가 'user_id'이고 value(키값)는 user.id 인 (딕셔너리와 유사? 한)데이터 저장'''
            '''session은 request와 마찬가지로 플라스크에서 자동으로 '''
            session['user_id'] = user.id
            '''라우트함수에서 역으로 url 주소추출 후 이 url 주소로 모듈연결'''
            '''mypage_views.py의 bp이름이 mypage, mapage_views.py의 라우트 함수들중 하나의 이름이 homepage'''
            '''mypage_views.py의 (라우트)함수 homepage 호출, flask 서버 구동중에는 영구히 사용 가능'''
            return redirect(url_for('mypage.homepage', user_name=user.username))
        flash(error)
    #request.method == 'GET'인 경우 (GET 요청 방식인 경우), 로그인 시도 없이 _login함수가 불려왔을 때
    return render_template('login.html', form=form)

@bp.route('/signup/', methods=('GET', 'POST'))
#form = UserCreateForm() 이 POST방식으로 데이터를 전송하기 때문에 라우트 함수의 methods 에 "POST"를 전달해야됌
def signup():
    '''계정 등록 페이지로 이동 및 계정 등록'''
    form = UserCreateForm()
    if request.method == 'POST' and form.validate():
        error = None
        if not User.query.filter_by(username=form.username.data).first(): #중복된 닉네임 걸러짐
            if not User.query.filter_by(userid=form.userid.data).first(): #중복된 id 걸러짐
                user = User(username=form.username.data,
                            userid=form.userid.data,
                            password=generate_password_hash(form.password1.data),
                            email=form.email.data)
                db.session.add(user)
                db.session.commit() #db변경사항 저장
                flash('회원가입이 완료되었습니다')
                return render_template(redirect(url_for('login._login'))) #로그인 화면으로 이동
            else:
                flash('중복된 ID 입니다')
        else:
            flash('중복된 닉네임입니다')
        

    return render_template('signup.html', form=form)

@bp.before_app_request
#라우트 함수보다 먼저 실행된다
def load_logged_in_user():
    user_id = session.get('user_id') #_login 함수에서 session[user_id] user.id (User 모델의 user.id, user.user_id가 아니다)
    if user_id is None:
        #g 는 플라스크에서 자동생성하는 전역변수이다
        g.user = None
    else:
        g.user = User.query.get(user_id)
