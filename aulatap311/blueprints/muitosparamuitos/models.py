from aulatap311.ext.database import db

noticiatag = db.Table('noticatag',
    db.Column('noticia_id', db.Integer, db.ForeignKey('noticia.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    )

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(2000), nullable=False)
    tags = db.relationship('Tag', secondary=noticiatag, backref=db.backref('noticias'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assunto = db.Column(db.String(10), nullable=False)