from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dataclasses import field
from gzip import READ
from unittest import result
from flask import Flask, jsonify, request
from conf import config
from flask_marshmallow import Marshmallow


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


from flask import Flask, jsonify, request

app = Flask(__name__)














class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NameRes = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(), nullable=True)
    informa = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    bookmarks = db.relationship('Bookmark', backref="user")

    def __repr__(self) -> str:
        return 'User>>>{self.NameRes}'


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return 'User>>>{self.Name}'


class InfoUser(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'NameRes',
                  'infoma', 'direccion', 'telefono')


infoUser = InfoUser()
infoUser = InfoUser(many=True)


@app.route('/add', methods=['POST'])
def add_rest():
    NameRes = request.json['NameRes']
    infoma = request.json['infoma']
    direccion = request.json['direccion']
    telefono = request.json['telefono']

    articles = User(NameRes, infoma, direccion, telefono)
    db.session.add(articles)
    db.session.commit()
    return infoUser.jsonify(articles)


@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = User.query.all()
    results = infoUser.dump(all_articles)
    return jsonify(results)


@app.route('/get/<id>/', methods=['GET'])
def post_detalles(id):
    article = User.query.get(id)
    return infoUser.jsonify(article)


@app.route('/update/<id>/', methods=['PUT'])
def update_article(id):
    article = User.query.get(id)

    NameRes = request.json['NameRes']
    infoma = request.json['infoma']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    article.NameRes = NameRes
    article.infoma = infoma
    article.direccion = direccion
    article.telefono = telefono

    db.session.commit()
    return infoUser.jsonify(article)


@app.route('/delete/<id>/', methods=['DELETE'])
def articles_delete(id):
    artitcle = User.query.get(id)
    db.session.delete(artitcle)
    db.session.commit()

    return User.jsonify(artitcle)







@app.route('/', methods=['GET'])
def lusta():
    try:
        return "ok"
    except Exception as ex:
        return "error"


def pagina404(error):
    return "<h1>Página no encontrada<h1/>"


if __name__ == "__main__":
    app.config.from_object(config['develoment'])
    app.register_error_handler(404, pagina404)
    app.run()
