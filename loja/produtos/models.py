from loja import db
from datetime import datetime

class Addproduto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'),nullable=False)
    marca = db.relationship('Marcas', backref=db.backref('marcas', lazy=True))

    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'),nullable=False)
    fornecedor = db.relationship('Fornecedor', backref=db.backref('fornecedores', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduto %r>' % self.name



class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    endereco = db.Column(db.String(50), nullable=False, unique=True)

class Marcas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False, unique=True)

db.create_all()