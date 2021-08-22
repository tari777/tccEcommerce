from loja import db

class Fornecedor(db.Model):
    forn_id = db.Column(db.Integer, primary_key=True)
    forn_razaoSocial = db.Column(db.String(50), nullable=False, unique=True)
    #forn_endereco = db.Column(db.String(50), nullable=False, unique=False)
    #forn_cnpj = db.Column(db.String(30), nullable=False, unique=True)
    #forn_ie = db.Column(db.String(30), nullable=False, unique=True)
    #forn_telefone = db.Column(db.String(30), nullable=False, unique=True)

db.create_all()