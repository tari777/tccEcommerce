from .forms import CadastroClienteForm, ClienteLoginForm
from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app, photos, bcrypt, login_manager
import secrets, os
from .model import Cadastrar
from flask_login import login_required, current_user, login_user, logout_user



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
        return redirect(url_for('login'))
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