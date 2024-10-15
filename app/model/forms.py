from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, SelectField, validators, DateField, RadioField, TextAreaField, FileField
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
    nome_aluno = StringField("Nome do Aluno", validators=[DataRequired()])
    data_atendimento = DateField("Data Atendimento", validators=[DataRequired()])
    nascimento_aluno = DateField("Data de Nascimento", validators=[DataRequired()])
    serie_aluno = StringField("Ano/Série", validators=[DataRequired()])
    parentesco_responsavel = StringField("Grau de Parentesco", validators=[DataRequired()])
    email_responsavel = EmailField("E-mail", validators=[DataRequired()])
    telefone_responsavel = StringField("Telefone", validators=[DataRequired()])
    celular_responsavel = StringField("Celular", validators=[DataRequired()])
    solicitado_por = RadioField("Solicitado Por", 
            choices=[('Pelos Responsáveis', 'Solicitação foi feita pelos responsáveis'), ('Pela Escola', 'Solicitação foi feita pela escola')], validators=[DataRequired()])
    questoes = TextAreaField("Questões")
    aconselhamento = TextAreaField("Aconselhamento / Observações da escola")
    providencias = TextAreaField("Providências")
    observacoes_finais = TextAreaField("Observações Finais")



class UpdateAtendimentoForm(FlaskForm):
    usuario = StringField("Nome do usuário")
    responsavel = StringField("Nome do responsável")
    tipo = SelectField("Tipo de Atendimento")
    situacao = SelectField("Situação do Atendimento")
    data_conclusao = DateField("Data de conclusão")
    retorno = StringField("Retorno para o usuário")