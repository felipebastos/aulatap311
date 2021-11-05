from flask import Blueprint, render_template
from aulatap311.blueprints.muitosparamuitos import models
from aulatap311.ext.database import db


bp = Blueprint('muitosparamuitos', __name__, url_prefix='/muitosparamuitos')


@bp.route('/')
def root():
    novaNoticia = models.Noticia()
    novaNoticia.texto = 'Essa é outra notícia'

    db.session.add(novaNoticia)
    db.session.commit()

    novaTag = models.Tag()
    novaTag.assunto = 'mais uma'

    aquejatinha = models.Tag.query.get(1)

    novaNoticia.tags.append(aquejatinha)
    novaNoticia.tags.append(novaTag)

    db.session.commit()

    return 'Hello from muitosparamuitos'

@bp.get('/noticias')
def noticias():
    todas = models.Noticia.query.all()

    return render_template('noticias.html', noticias=todas)


def init_app(app):
    app.register_blueprint(bp)