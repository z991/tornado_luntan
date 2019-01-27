from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

MOBILE_REGEX = "^1[358]\d{9}$|^1[48]7\d{8}$|^176\d{8}$"

class SmsCodeForm(Form):
    mobile = StringField("手机号", validators=[DataRequired(message="请输入手机号"), Regexp(MOBILE_REGEX, message="请输入合法的手机号")])