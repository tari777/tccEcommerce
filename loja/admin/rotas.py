from loja.admin.models import User
from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Addproduto
from loja import app, db, bcrypt
from .forms import RegistrationForm, LoginFormulario
from .models import User
import os

 

@app.route('/')
def admin():
    if'email' not in session: #SE O EMAIL N EXISTE
        flash(f'Favor fazer seu login primeiro', 'success')
        flash('Logue no sistema primeiro', 'danger') 
        return redirect(url_for('login')) #VAI PARA A TELA DE LOGIN
    produtos = Addproduto.query.all()
    return render_template ('admin/index.html', title="Pagina Administrativa", produtos=produtos)


    
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)   
        user = User(name = form.name.data, username=form.username.data, email = form.email.data,
        password = hash_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Obrigado {form.username.data} por registrar', 'success') 

        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Página de Registros")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #CHECA A SENHA ENCRYPTOGRAFADA
            session['email'] = form.email.data
            flash(f'Logado com {form.email.data}!', 'success') 
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('Não foi possivel logar no sistema!', 'danger') 

    return render_template ('admin/login.html', form=form, title='Pagina Login')


