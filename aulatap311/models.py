from aulatap311.ext.database import db
from aulatap311.ext.login import loginmanager

from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    imagem_perfil = db.Column(db.String(100), default='padrao.png')

@loginmanager.user_loader
def abre_usuario(id):
    return Usuario.query.get(id)
