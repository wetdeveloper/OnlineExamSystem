from app import *
class SignupForm(FlaskForm):   
      # username = StringField('username', [validators.DataRequired(), validators.Length(max=64)])
      # password = PasswordField('password', [validators.DataRequired(),validators.Length(min=8)])
      # submit=SubmitField('Signup')
      recaptcha = RecaptchaField()


class LoginForm(FlaskForm):   
      # username = StringField('username', [validators.DataRequired(), validators.Length(max=64)])
      # password = PasswordField('password', [validators.DataRequired(),validators.Length(min=8)])
      # submit=SubmitField('Login')
      recaptcha = RecaptchaField()


class forgetpasswordForm(FlaskForm):
      recaptcha = RecaptchaField()

class resetpasswordForm(FlaskForm):
      recaptcha= RecaptchaField()