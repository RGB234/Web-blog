from flask import Blueprint, url_for, render_template, request, session
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash

from ..forms import UserLoginForm
from ..models import User

bp = Blueprint('login', __name__, url_prefix='/')

@bp.route('/login/', methods=('GET', 'POST'))
def _submit():
    
    ''' login.html 렌더링(request.method == 'GET') '''
    ''' 로그인 양식(UserLoginform)을 적절하게 채워서 제출(request.method == 'Post')하면 mypage.homepage호출'''
    ''' 어떤 경우에 GET / POST 요청이 들어오는지는 login.html에 구현'''

    form = UserLoginForm()
    #request는 flask에서 자동제공 참조:https://velog.io/@sangmin7648/%EC%98%A4%EB%8A%98%EC%9D%98-%EB%B0%B0%EC%9B%80-045
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first() #검색
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
            return redirect(url_for('mypage.homepage'))
    #request.method == 'GET'인 경우, (GET 요청 방식인 경우)
    return render_template('login.html', form=form)

    