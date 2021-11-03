import os
from flask import Blueprint, render_template, request, send_from_directory
from sqlalchemy import log

from aulatap311.models import Usuario

from aulatap311.app import create_app

from aulatap311.ext.database import db

from flask_login import login_user, login_required, current_user


bp = Blueprint('cadastro', __name__, url_prefix='/cadastro', template_folder='templates')

FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


@bp.route('/')
def root():
    return render_template('cadastro/cadastro.html')


@bp.post('/add')
def adicionaNovoUsuario():
    nome = request.form['nome']
    senha = request.form['senha']

    if 'fotoperfil' not in request.files:
        return "Sai daí! Tá errado!"
    foto = request.files['fotoperfil']
    if foto and allowed_file(foto.filename):
        novo = Usuario()
        novo.nome = nome
        novo.senha = senha
        novo.imagem_perfil = foto.filename

        app = create_app()
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto.filename))

        db.session.add(novo)
        db.session.commit()

        return 'Deu certo com foto!'
    else:
        novo = Usuario()
        novo.nome = nome
        novo.senha = senha

        db.session.add(novo)
        db.session.commit()

        return 'Deu certo sem foto!'

@bp.route('/login', methods=['GET', 'POST'])
def logar():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        quem = Usuario.query.filter_by(nome=nome).first()

        if quem.senha == senha:
            login_user(quem)
            return 'Logou'
        return 'não logou'
    return render_template('cadastro/login.html')

@bp.get('/perfil')
@login_required
def perfil():
    return render_template('cadastro/perfil.html')

@bp.get('/imagem/<nome>')
@login_required
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_FOLDER'], nome)

@bp.get('/removefoto')
@login_required
def removefoto():
    if current_user.imagem_perfil != 'padrao.png':
        app = create_app()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.imagem_perfil))

        current_user.imagem_perfil = 'padrao.png'

        db.session.add(current_user)
        db.session.commit()

        return 'Removi a foto'
    return 'Não removi a foto'

@bp.route('/edita', methods=['GET', 'POST'])
@login_required
def editaperfil():
    if request.method == 'POST':
        if 'fotoperfil' not in request.files:
            return "Sai daí! Tá errado!"
        foto = request.files['fotoperfil']
        if foto and allowed_file(foto.filename):
            if current_user.imagem_perfil != 'padrao.png':
                app = create_app()
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.imagem_perfil))

            current_user.imagem_perfil = foto.filename
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto.filename))

            db.session.add(current_user)
            db.session.commit()
            return 'Foto de perfil atualizada'
    return render_template('cadastro/edita.html')


def init_app(app):
    app.register_blueprint(bp)