  
from loja.produtos.models import Fornecedor
from .forms import Addprodutos
from flask import redirect, render_template, url_for, flash, request, session
from .models import Fornecedor, Marcas, Addproduto
from loja import db, app, photos
import secrets




@app.route('/addmarca', methods=['GET', 'POST'])   
def addmarca():
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marcas(name=getmarca)
        db.session.add(marca)
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')



@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])   
def updatemarca(id):
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN
    updatemarca = Marcas.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method=='POST':
        updatemarca.name = marca
        flash(f'Sua marca foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    return render_template('/produtos/updatemarca.html', title='Atualizar Marca', updatemarca=updatemarca)


@app.route('/updateforn/<int:id>', methods=['GET', 'POST'])   
def updateforn(id):
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN
    updateforn = Fornecedor.query.get_or_404(id)
    fornecedor = request.form.get('fornecedor')
    if request.method=='POST':
        updateforn.name = fornecedor
        flash(f'Seu Fabricante foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('fornecedor'))
    return render_template('/produtos/updatemarca.html', title='Atualizar Fornecedor', updateforn=updateforn)

@app.route('/addforn', methods=['GET', 'POST'])   
def addforn():
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN
         
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
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN
    marcas = Marcas.query.all()
    fornecedores = Fornecedor.query.all()
    form = Addprodutos(request.form)
    if request.method=="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        marca = request.form.get('marca')
        fornecedor = request.form.get('fornecedor')

        image_1 = photos.save(request.files.get('image_1'), name= secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name= secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name= secrets.token_hex(10)+".")

        addpro = Addproduto(name=name,price=price,discount=discount,stock=stock,desc=desc, marca_id = marca, fornecedor_id=fornecedor, image_1 = image_1, image_2 = image_2, image_3 = image_3)
        db.session.add(addpro)
        flash(f'O produto {name} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
        
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form = form, marcas = marcas, fornecedores = fornecedores)