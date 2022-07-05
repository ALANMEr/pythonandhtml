import imp
from pydoc import render_doc
from flask import Flask, flash, redirect, render_template
from gzip import READ
from unittest import result
from flask import Flask, jsonify, request,url_for,flash
from sqlalchemy import join
from conf import config
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import Model, SQLAlchemy
from models.ModelUser import ModelUser
from models.entities import User
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)






class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NameRes = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(), nullable=True)
    informa = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, NameRes,email,password, informa, direccion, telefono):
        self.NameRes = NameRes 
        self.email=email
        self.password=password
        self.informa = informa
        self.direccion = direccion
        self.telefono = telefono


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(), nullable=True)
    posts=db.relationship('Posts',backref='poster')

    def __init__(self,Name,email,password):
        self.Name=Name
        self.email=email
        self.password=password

#Restaurante registro
class InfoUser(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'NameRes','infoma', 'direccion', 'telefono')


infoUser = InfoUser()
infoUser = InfoUser(many=True)


#USARIO REGISTRO
class InfoUsuario(ma.Schema):
    class Meta:
        fields = ('id', 'Name', 'email', 'password')

infoRestaurante = InfoUsuario()
infoRestaurante = InfoUsuario(many=True)



#Registro restaurante
@app.route('/add', methods=['POST'])
def add_rest():
    NameRes = request.json['NameRes']
    email=request.json['email']
    password = request.json['password']
    informa = request.json['informa']
    direccion = request.json['direccion']
    telefono = request.json['telefono']

    articles = Posts(NameRes, email, password, informa, direccion, telefono)
    db.session.add(articles)
    db.session.commit()
    return infoUser.jsonify(articles)

#Registro Usuario


@app.route('/login', methods=['POST'])
def add_login():
 
    Name = request.json['Name']
    email = request.json['email']
    password = request.json['password']
 
  
    articles1 = Users(Name, email, password)
    db.session.add(articles1)
    db.session.commit()
    return infoUser.jsonify(articles1)
    
    
  #Buscar todos los usuarios  
@app.route('/log', methods=['GET'])
def get_articles1():
    all_articles = Users.query.all()
    results = infoUser.dump(all_articles)
    return jsonify(results)


#Muestra todos los restaurantes
@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Posts.query.all()
    results = infoUser.dump(all_articles)
    return jsonify(results)

#Muestra solo un restaurante por el id
@app.route('/get/<id>/', methods=['GET'])
def post_detalles(id):
    article = Posts.query.get(id)
    return infoUser.jsonify(article)


#Muestra solo un usuario
@app.route('/log/<id>/', methods=['GET'])
def post_detalless(id):
    article = Users.query.get(id)
    return infoUser.jsonify(article)
#Edita los restaurantes
@app.route('/update/<id>/', methods=['PUT'])
def update_article(id):
    article = Posts.query.get(id)

    NameRes = request.json['NameRes']
    informa = request.json['informa']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    article.NameRes =NameRes
    article.infoma = informa
    article.direccion = direccion
    article.telefono = telefono

    db.session.commit()
    return infoUser.jsonify(article)



#Borra los restaurantes
@app.route('/delete/<id>/', methods=['DELETE'])
def articles_delete(id):
    artitcle = Posts.query.get(id)
    db.session.delete(artitcle)
    db.session.commit()

    return Posts.jsonify(artitcle)

@app.route('/', methods=['GET'])
def lusta():
    try:
        return "Inicio"
    except Exception as ex:
        return "error"


def pagina404(error):
    return "<h1>Página no encontrada<h1/>"


#Metodos
 
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/usu', methods=['GET','POST'])
def usu():
    if request.method=='POST':
        user=User(0,request.form['Name'],request.form['password'])
       
        logged_user=ModelUser.login(db,user)
        if logged_user == None:
            if logged_user.password:
                return redirect(url_for('/frondend/client.html'))
            else:
                     flash("Password no valido")
                     return render_template('/frondend/index.html')
        else:
             flash("No se encontro")
    else:
             return render_template('/frondend/index.html')




@app.route('/home')
def home():
    return render_template('')


if __name__ == "__main__":
    app.config.from_object(config['develoment'])
    app.register_error_handler(404, pagina404)
    app.run('/ frondend/index.html')
