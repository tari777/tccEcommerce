from loja.produtos.models import Fornecedor
from .forms import Addprodutos
from flask import redirect, render_template, url_for, flash, request
from .models import Fornecedor
from loja import db, app


@app.route('/addforn', methods=['GET', 'POST'])
def addforn():
    if request.method == "POST":
        getforn = request.form.get('fornecedor') #ESSE fornecedor vem da pagina html onde o input tem o campo fornecedor
        forn = Fornecedor(forn_razaoSocial = getforn)
        db.session.add(forn)
        flash(f'O fornecedor {getforn} foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addforn'))
    return render_template('/produtos/addforn.html', forn='forn') 


@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    form = Addprodutos(request.form)
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form = form)
   
