from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, PasswordField, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from .model import Cadastrar


class CadastroClienteForm(FlaskForm):
    name = StringField('Nome :')
    username = StringField('Usuário :', [validators.DataRequired()])
    email = StringField('Email :', [validators.DataRequired()],  render_kw={"placeholder": "Email"})
    password = PasswordField('Senha : ',[validators.DataRequired(),validators.EqualTo('confirm', message='As senhas devem ser iguais!')],  render_kw={"placeholder": "Senha"})
    confirm = PasswordField('Repetir Senha: ', [validators.DataRequired()])
    country = StringField('País: ', [validators.DataRequired()])
    state = StringField('Estado: ', [validators.DataRequired()])
    city = StringField('Cidade: ', [validators.DataRequired()])
    contact = StringField('Telefone: ', [validators.DataRequired()])
    adress = StringField('Endereço: ', [validators.DataRequired()])
    zipcode = StringField('CEP: ', [validators.DataRequired()]) 
    profile = FileField('Perfil', validators=[FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        if Cadastrar.query.filter_by(username = username.data).first():
            raise ValidationError("Este usuário já existe no banco de dados")
            
    def validate_email(self, email):
        if Cadastrar.query.filter_by(email = email.data).first():
            raise ValidationError("Este email já existe no banco de dados")
            
       
class ClienteLoginForm(FlaskForm):
    email = StringField('Email :', [validators.DataRequired()])
    password = PasswordField('Senha : ',[validators.DataRequired()])
   