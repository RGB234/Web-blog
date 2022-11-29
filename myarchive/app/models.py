from app import db #__init__.py 에서 생성한 SQLALchemy 객체

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary_key 속성의 기본 키(db상의 id)로 지정
    userid = db.Column(db.String(60), unique=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    