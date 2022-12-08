from app import db #__init__.py 에서 생성한 SQLALchemy 객체

class User(db.Model):
    '''primary_key 속성을 가진 id는 자동으로 값이 커짐'''
    id = db.Column(db.Integer, primary_key=True, nullable=False) 
    '''
    #primary_key 속성의 기본 키(db상의 id)로 지정 autoincrement
    nullable=False 속성 사용시 유의점: https://wikidocs.net/81059
    '''
    username = db.Column(db.String(60), unique=True, nullable=False)
    userid = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    