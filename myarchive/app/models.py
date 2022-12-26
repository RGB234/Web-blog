from app import db #__init__.py 에서 생성한 SQLALchemy 객체

# SQLAlchemy Models(One-to-Many, Many-to-One, Many-to-Many)
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many

class User(db.Model): #유저계정
    '''primary_key 속성을 가진 id는 자동으로 값이 커짐'''
    id = db.Column(db.Integer, primary_key=True) 
    '''
    #primary_key 속성을 통해 해당 칼럼을 db 모델의 기본 키(id)로 지정
    nullable=False 속성 사용시 유의점과 해결: https://wikidocs.net/81059 / 이전에 null 값을 포함한 칼럼을 nullable=False로 할 경우 충돌발생
    db column 이 unique 속성을 가질 경우, 중복되는(unique하지 않은)값은 오류가 발생하며 db에 추가되지 않음 (예외처리가 필요)
    '''
    username = db.Column(db.String(60), unique=True, nullable=False)
    userid = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Post(db.Model): #작성한 글
    id = db.Column(db.Integer, primary_key=True) #id
    subject = db.Column(db.String(200), nullable=False) #제목
    content = db.Column(db.Text(), nullable=False) #내용, Text형은 길이제한 x
    create_date = db.Column(db.DateTime(), nullable=False) #작성일
    modify_date = db.Column(db.DateTime(), nullable=True) #수정일
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    #user id 는 User모델의 id칼럼을 참조하여 만든 Post db의 칼럼, User모델을 참조하기 위해 필요
    #ondelete는 삭제연동기능
    #ondelete = 'CASCADE' Post 객체와 연동된 USER 객체가 삭제되면 연동되있는 POST객체도 삭제
    #즉, 데이터베이스 명령으로 User 계정하나가 삭제되면 작성했던 글도 삭제된다
    user = db.relationship('User', backref=db.backref('post_set')) #작성자
    #User모델 객체에서 .Post_set(backref) 을 통해 연결(relationship)된 Post객체를 불러올 수 있다

class Category(db.Model): #글 분류 카테고리
    id = db.Column(db.Integer, primary_key=True)
    big_category = db.Column(db.String(100), nullable=True, server_default='None') #대분류
    small_category = db.Column(db.String(100), nullable=True, server_default='None') #소분류
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    #Category 객체가 삭제되면 연결된 Post 객체의 Category 객체는 None(big)-None(small)이 되어야 한다
    post = db.relationship('Post', backref=db.backref('category_set'))

class Comment(db.Model): #글의 댓글
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False) #댓글 내용
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False) #댓글이 달린 글의 id
    post = db.relationship('Post', backref=db.backref('comment_set')) #댓글이 달린 글