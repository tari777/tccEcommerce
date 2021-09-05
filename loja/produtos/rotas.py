  
from loja.produtos.models import Fornecedor
from .forms import Addprodutos
from flask import redirect, render_template, url_for, flash, request
from .models import Fornecedor, Marcas
from loja import db, app, photos




@app.route('/addmarca', methods=['GET', 'POST'])   
def addmarca():
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')


@app.route('/addforn', methods=['GET', 'POST'])   
def addforn():
    if request.method == "POST":
        getmarca = request.form.get('fornecedor')
        getend = request.form.get('endereco')
        forn = Fornecedor(name=getmarca, endereco = getend)
        db.session.add(forn)
        flash(f'O fornecedor {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addforn'))
    return render_template('/produtos/addmarca.html')



@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    marcas = Marcas.query.all()
    fornecedores = Fornecedor.query.all()
    form = Addprodutos(request.form)
    if request.method=="POST":
        photos.save(request.files.get('image_1'))
        photos.save(request.files.get('image_2'))
        photos.save(request.files.get('image_3'))
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form = form, marcas = marcas, fornecedores = fornecedores)