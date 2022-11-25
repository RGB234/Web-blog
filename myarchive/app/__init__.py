from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .views import login_views, mypage_views 

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

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE') #myarchive.cmd에서 APP_CONFIG_FILE = development.py 로 설정

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    #blueprint
    from .views import login_views
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(login_views.bp)

    return app

