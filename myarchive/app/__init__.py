from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
 
'''
SQLAlchemy 이름을 랜덤으로 형성할 때의 제약조건, 
이 제약이 없으면 SQLite에서는 "Constraint must have a name"라는 오류발생 
(MySQL, PostgreSQL과는 무관)
reference: https://alembic.sqlalchemy.org/en/latest/naming.html
'''
naming_convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
'''db, migrate를 전역으로 정의(다른 모듈에서 불러올 수 있음)하고 초기화는 create_app함수 내부에서 실행'''

def page_not_found(e):
      return render_template('404.html'), 404

def create_app(): #애플리케이션 팩토리 함수, 반드시 create_app()으로 이름을 지어야 한다(flask 내부에서 정의된 함수명)
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE') #myarchive.cmd에서 APP_CONFIG_FILE = development.py 로 설정
    #envvar == environment variable
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    # render_as_batch = True 를 해야 Error:No support for ALTER of constraint in SQLite dialect 가 뜨지않음
    # if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):   // 'SQLALCHEMY_DATABASE_URI' config/development.py 에서 정의됨
    #       migrate.init_app(app, db, render_as_batch=True)
    # else:
    #       migrate.init_app(app, db)

    #blueprint
    from .views import login_views, mypage_views
    app.register_blueprint(login_views.bp)
    app.register_blueprint(mypage_views.bp)

    #오류페이지
    app.register_error_handler(404, page_not_found)

    # 필터
    from .filter import format_datetime
    #datetime 이라는 이름으로 템플릿 필터 format_datetime 등록
    app.jinja_env.filters['datetime'] = format_datetime

    return app

