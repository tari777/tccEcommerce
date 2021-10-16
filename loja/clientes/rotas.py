from .forms import CadastroClienteForm, ClienteLoginForm
from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from loja import db, app, photos, bcrypt, login_manager
import secrets, os
from .model import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
import stripe
from loja.produtos.rotas import marcas, fornecedores

publishtable_key = 'pk_test_51JkhNsJNRIMOxPTeepB3tQZHLsV3IIVueEAjLixx7OaGiUBH5C0FUF6af8I6YNmS8Q3sBNLSylkIf5YOLZ6ebKXO00j0WJjdoc'
stripe.api_key = 'sk_test_51JkhNsJNRIMOxPTetlMs81PJADVxZBw2zcbz76Vc1D1DJiLMlCK9zmUtiib0LUm5J5ocMqiLXxbkmZcA0ZFXgWJc00AybpckOR'

@app.route('/pagamento', methods=['POST']) 
@login_required
def pagamento():
    notafiscal = request.form.get('invoice')
    amount = request.form.get('amount')

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
        )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='TCC LOJA',
        amount=amount,
        currency='brl',
        )
    cliente_pedido = ClientePedido.query.filter_by(cliente_id = current_user.id, notafiscal = notafiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status='Pago'
    db.session.commit()
    return redirect(url_for('obrigado'))

@app.route('/obrigado') 
def obrigado():
    return render_template('cliente/obrigado.html')

@app.route('/cliente/cadastrar', methods=['GET', 'POST']) 
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username = form.username.data, email=form.email.data,
        password = hash_password, confirm = form.confirm.data, country = form.country.data, state = form.state.data, city = form.city.data, contact = form.contact.data, adress = form.adress.data, zipcode = form.zipcode.data, profile = form.profile.data )
        db.session.add(cadastrar)
        flash(f'Obrigado {form.name.data} por se cadastrar', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/cliente.html', form = form)



@app.route('/cliente/login', methods=['GET', 'POST']) 
def clienteLogin():
    form = CadastroClienteForm(request.form)
    if request.method == 'POST':
        user = Cadastrar.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Você está logado', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Informações incorretas!', 'danger')
        return redirect(url_for(clienteLogin))

    return render_template('cliente/login.html', form = form)



@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))


def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        
    return atualizarlojaCarro


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated: 
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        atualizarlojaCarro()
        try:
            p_order = ClientePedido(notafiscal = notafiscal, cliente_id = cliente_id, pedido = session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            return redirect(url_for('pedidos', notafiscal = notafiscal, marcas = marcas(), fornecedores = fornecedores()))
            
        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido!', 'danger')
            return redirect(url_for('getCart'))

@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated: 
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Cadastrar.query.filter_by(id = cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id = cliente_id, notafiscal = notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key , produto in pedidos.pedido.items():    
            disconto = (produto['discount']/100) * float(produto['price'])
            subTotal += float(produto['price']) * int(produto['quantity'])
            subTotal -= disconto
            imposto = ("%.2f" % (.06* float(subTotal)))
            gTotal = ("%.2f" % (1.06 * subTotal))
    else:
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/pedido.html', notafiscal = notafiscal, imposto = imposto, subTotal = subTotal, gTotal = gTotal, cliente = cliente, pedidos = pedidos, marcas = marcas(), fornecedores = fornecedores())


@app.route('/get_pdf/<notafiscal>', methods = ['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated: 
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        if request.method=="POST":
            cliente = Cadastrar.query.filter_by(id = cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id = cliente_id, notafiscal = notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key , produto in pedidos.pedido.items():    
                disconto = (produto['discount']/100) * float(produto['price'])
                subTotal += float(produto['price']) * int(produto['quantity'])
                subTotal -= disconto
                imposto = ("%.2f" % (.06* float(subTotal)))
                gTotal = ("%.2f" % (1.06 * subTotal))
            rendered = render_template('cliente/pdf.html', notafiscal = notafiscal, imposto = imposto, subTotal = subTotal, gTotal = gTotal, cliente = cliente, pedidos = pedidos)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'attched;filename='+notafiscal+'.pdf'
            return response
    return redirect(url_for('pedidos'))