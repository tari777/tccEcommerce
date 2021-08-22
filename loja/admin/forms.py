from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Nome Completo', [validators.Length(min=4, max=25)])
    username = StringField('Nick', [validators.Length(min=6, max=35)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.InputRequired (), validators.EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')


class LoginFormulario(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Senha', [validators.DataRequired()])

