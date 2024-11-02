from ConviteDigital import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String,nullable = False,unique=True)
    senha = database.Column(database.String,nullable = False)
    pagamento = database.Column(database.String)
    foto = database.relationship("Foto", backref="usuario", lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    imagem = database.Column(database.String,default="default.png")
    data = database.Column(database.DateTime, nullable = False, default=datetime.now())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),nullable = False)

class Pagamento_Simplificado(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    convidados = database.Column(database.String,nullable = False)
    quantidade = database.Column(database.String,nullable = False)
    idpag = database.Column(database.String)
    status = database.Column(database.String)