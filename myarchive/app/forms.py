from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserLoginForm(FlaskForm):
    id = StringField('아이디', validators=[DataRequired('닉네임을 입력하십시오'), Length(min=3, max=12)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력하십시오')])

class UserCreateForm(FlaskForm):
    id = StringField('아이디', validators=[DataRequired('닉네임을 입력하십시오'), Length(min=3, max=12)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력하십시오')])
    password2 = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력하십시오'), EqualTo('password1', '비밀번호가 일치하지 않습니다')])
    email = EmailField('이메일', validators=[DataRequired('이메일을 입력하십시오'), Email()])