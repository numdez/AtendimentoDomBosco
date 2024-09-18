from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, SelectField, validators, DateField, FloatField, TextAreaField, FileField
from wtforms.validators import DataRequired, InputRequired, Optional

# Login
class LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    lembrar = BooleanField("Lembrar de mim")
    next = StringField()

class AddUsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    segredo = StringField("Auth")
    tipo = SelectField("Tipo de usuário")

class UpdateUsuarioForm(FlaskForm):
    nome = StringField("Nome")
    email = EmailField("E-mail")
    senha = PasswordField("Senha")
    tipo = SelectField("Tipo de usuário")

class AddAtendimentoForm(FlaskForm):
    data_criacao = DateField("Data de criação", validators=[DataRequired()])
    usuario = StringField("Nome do usuário")
    tipo = SelectField("Tipo de Atendimento", validators=[DataRequired()])
    requisicao = StringField("Requisição", validators=[DataRequired()])

class UpdateAtendimentoForm(FlaskForm):
    usuario = StringField("Nome do usuário")
    responsavel = StringField("Nome do responsável")
    tipo = SelectField("Tipo de Atendimento")
    situacao = SelectField("Situação do Atendimento")
    data_conclusao = DateField("Data de conclusão")
    retorno = StringField("Retorno para o usuário")