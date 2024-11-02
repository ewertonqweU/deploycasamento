from numbers import Number

from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, FileField
from wtforms.validators import  DataRequired, EqualTo, length, ValidationError
from ConviteDigital.models import Usuario

class FormLogin(FlaskForm):
    user = StringField("Usuario",validators=[DataRequired()])
    senha = PasswordField("Senha",validators=[DataRequired()])
    botao_conf = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    user = StringField("Usuario",validators=[DataRequired()])
    senha = PasswordField("Senha",validators=[DataRequired()])
    confirmacao_senha = PasswordField("Confirmação de Senha",validators=[DataRequired(), EqualTo("senha")])
    botao_conf = SubmitField("Criar Conta")

    def validate_user(self, user):
        usuario = Usuario.query.filter_by(username=user.data).first()
        if usuario:
            return  ValidationError("Usuario ja esta em uso")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_conf = SubmitField("enviar")


class FormPGF(FlaskForm):
    convidados = StringField("Convidados",validators=[DataRequired()])
    qtd = StringField("Quantidade",validators=[DataRequired()])
    botao_conf = SubmitField("Gerar Pagamento")