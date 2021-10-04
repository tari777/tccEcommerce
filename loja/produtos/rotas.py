  
from loja.produtos.models import Fornecedor
from .forms import Addprodutos
from flask import redirect, render_template, url_for, flash, request, session, current_app
from .models import Fornecedor, Marcas, Addproduto
from loja import db, app, photos
import secrets, os




@app.route('/')
def home():
    pagina = request.args.get('pagina', 1, type=int)
    produtos = Addproduto.query.filter(Addproduto.stock > 0).order_by(Addproduto.id.desc()).paginate(page=pagina,per_page=4)
    marcas = Marcas.query.join(Addproduto, (Marcas.id==Addproduto.marca_id)).all()
    fornecedores = Fornecedor.query.join(Addproduto, (Fornecedor.id==Addproduto.fornecedor_id)).all()
    return render_template('produtos/index.html', produtos = produtos, marcas = marcas, fornecedores=fornecedores)



@app.route('/marca/<int:id>') 
def get_marca(id):
    get_m = Marcas.query.filter_by(id = id).first_or_404()
    pagina = request.args.get('pagina', 1, type=int)
    marca = Addproduto.query.filter_by(marca = get_m).paginate(page=pagina,per_page=4)
    marcas = Marcas.query.join(Addproduto, (Marcas.id==Addproduto.marca_id)).all()
    fornecedores = Fornecedor.query.join(Addproduto, (Fornecedor.id==Addproduto.fornecedor_id)).all()
    return render_template('/produtos/index.html', marca=marca, marcas=marcas, fornecedores=fornecedores, get_m = get_m)

@app.route('/produto/<int:id>') 
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)
    return render_template('/produtos/pagina_unica.html', produto = produto)

@app.route('/fornecedor/<int:id>') 
def get_fornecedor(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_forn = Fornecedor.query.filter_by(id = id).first_or_404()
    get_forn_prod = Addproduto.query.filter_by(fornecedor = get_forn).paginate(page=pagina,per_page=4)
    marcas = Marcas.query.join(Addproduto, (Marcas.id==Addproduto.marca_id)).all()
    fornecedores = Fornecedor.query.join(Addproduto, (Fornecedor.id==Addproduto.fornecedor_id)).all()
    return render_template('/produtos/index.html', get_forn_prod=get_forn_prod, fornecedores=fornecedores, marcas=marcas, get_forn = get_forn)

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

@app.route('/deletemarca/<int:id>', methods=['POST'])   
def deletemarca(id):
    marca = Marcas.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(marca)
        db.session.commit()
        flash(f'A marca {marca.name} foi excluida com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A marca {marca.name} não foi excluida"', 'warning')
    return redirect(url_for('admin'))


@app.route('/deleteforn/<int:id>', methods=['POST'])   
def deleteforn(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(fornecedor)
        db.session.commit() 
        flash(f'A marca {fornecedor.name} foi excluida com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A marca {fornecedor.name} não foi excluida"', 'warning')
    return redirect(url_for('admin'))

@app.route('/deleteproduto/<int:id>', methods=['POST'])   
def deleteproduto(id):
    produto = Addproduto.query.get_or_404(id)
    if request.method=='POST':
         if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_3))
            except Exception as e:
                print(e)
         
         db.session.delete(produto)
         db.session.commit()
         return redirect(url_for('admin'))
    flash(f'Produto {produto.name} foi cadastrado com sucesso', 'success')

    return redirect(url_for('admin'))

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



    
@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])   
def updateproduto(id):
    marcas = Marcas.query.all()
    fornecedores = Fornecedor.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    fornecedor = request.form.get('fornecedor')
    form = Addprodutos(request.form)
    if request.method == "POST":
        produto.name = form.name.data
        produto.price = form.price.data
        produto.desc = form.description.data

        produto.marca_id = marca
        produto.fornecedor_id = fornecedor

        produto.stock = form.stock.data
        produto.discount = form.discount.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name= secrets.token_hex(10)+".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name= secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name= secrets.token_hex(10)+".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name= secrets.token_hex(10)+".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/"+produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name= secrets.token_hex(10)+".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name= secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'O produto foi atualizado com sucesso', 'success')
        return redirect(url_for('admin'))

    form.name.data = produto.name
    form.price.data = produto.price
    form.description.data = produto.desc
    form.stock.data = produto.stock
    form.discount.data = produto.discount

    


    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form, marcas=marcas, fornecedores=fornecedores, produto=produto)