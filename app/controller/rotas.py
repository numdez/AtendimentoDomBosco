from app.model.ModelUser import ModelUser
from app.controller.auth import Auth
from app.utils import utils
from app.model import functions
from app.model.forms import LoginForm
from app.model.entidades.Usuario import Usuario
from app.log.logger import log_action

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os

import base64
from io import BytesIO
from PIL import Image

from flask_login import logout_user, login_user, login_required, current_user
from flask import render_template, flash, redirect, url_for, request, abort, session, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
from datetime import timedelta
from pandas import DataFrame
from app import app, lm



# Login_manager
@lm.user_loader
def load_user(id):
    db_loader = ModelUser()
    lm.session_protection = "strong"
    data = ModelUser.get_by_id(db_loader, id)
    return data


# ROUTE
# Login
@app.route("/", methods=["GET", "POST"])
def index():
    db = ModelUser()
    form = LoginForm()
    next_url = form.next.data 
    if current_user.is_authenticated:
        if next_url:
            return redirect(next_url)
        session['ultAbaAberta'] = 'home'
        return redirect(url_for('home'))
    if form.validate_on_submit():
        if next_url:
            return redirect(next_url)
        user = Usuario(0, form.email.data, form.senha.data)
        logged_user = ModelUser.login(db, user)
        db._conn.close()
        if logged_user != None:
            if logged_user.senha:
                login_user(logged_user, remember=False)
                log_action(logged_user.nome, 'LOGIN')
                next = request.args.get('next')
                print(next)
                session['ultAbaAberta'] = 'home'
                return redirect(url_for("home"))
            else:
                flash("Senha incorreta. Verifique e tente novamente.")

        else:
            flash("Usuário não encontrado.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    user = functions.get_usuario(current_user.id)
    logout_user()
    log_action(user[0][1], 'LOGOUT')
    session.clear()
    resp = make_response(redirect(url_for("index")))
    return resp


@app.route("/home", methods=["GET", "POST"])
def home():
    id_user = session["_user_id"]
    current_user.mostra_valores()
    functions.loga_usuario(id_user)
    session['ultAbaAberta'] = 'home'
    usuario = utils.to_df(functions.get_usuario(id_user), 'usuario')
    return render_template('base.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Dados do formulário original
        nome = request.form['nome']
        email = request.form['email']
        assinaturaArquivo = request.files.get('assinaturaArquivo')

        # Se o usuário fizer upload da assinatura eletrônica
        if assinaturaArquivo and assinaturaArquivo.filename != '':
            filename = assinaturaArquivo.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            assinaturaArquivo.save(file_path)
            flash('Upload de assinatura bem-sucedido!')
        else:
            file_path = None

        # Redireciona para a página de assinatura com os dados do formulário
        return render_template('assinatura.html', nome=nome, email=email, assinatura=file_path)

    return render_template('formulario.html')

@app.route('/assinatura', methods=['GET', 'POST'])
def assinatura():
    if request.method == 'POST':
        # Verifique se foi desenhada uma assinatura
        assinatura_canvas = request.form.get('assinaturaCanvasData')

        # Verifique se um arquivo foi enviado
        arquivo = request.files.get('assinaturaArquivo')

        if assinatura_canvas:
            # Processa a assinatura desenhada
            # Aqui você pode salvar a imagem base64 ou processá-la
            flash('Assinatura desenhada recebida com sucesso!', 'success')
            return redirect(url_for('assinatura'))  # Redireciona para a mesma página

        elif arquivo:
            # Salva o arquivo de assinatura enviado
            filename = secure_filename(arquivo.filename)
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Arquivo de assinatura enviado com sucesso!', 'success')
            return redirect(url_for('assinatura'))  # Redireciona para a mesma página

        else:
            flash('Nenhuma assinatura fornecida. Por favor, desenhe ou envie um arquivo.', 'warning')
            return redirect(url_for('assinatura'))  # Redireciona para a mesma página

    # Se for uma solicitação GET, apenas renderize a página
    return render_template('assinatura.html')

@app.route('/teste')
def teste():
    return render_template('testeBase.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/atendimentos')
def atendimentos():
    return render_template('atendimentos.html')

@app.route('/requisicoes')
def requisicoes():
    return render_template('requisicoes.html')

@app.route('/requisitar')
def requisitar():
    return render_template('requisitar.html')

def save_signature(signature_data):
    import base64
    from io import BytesIO
    from PIL import Image
    # Extrair a imagem base64 (assume que a string tem o prefixo "data:image/png;base64,")
    signature_data = signature_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(signature_data)
    image = Image.open(BytesIO(image_data))
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'assinatura_desenhada.png'))

# FUNCTIONS HTTP
def status_404(error):
    return "<h1>Pagina não encontrada</h1>", 404

def status_403(error):
    return "<h1>Sistema pausado</h1>", 403

def status_500(error):
    return "<h1>Sistema em Manutenção</h1>", 500

@app.errorhandler(500)
def erro_interno(error):
    print('deu erro interno:', error)
    #return redirect(url_for('home'))

@app.errorhandler(401)
def page_not_auto(error):
    return "<h3>Acesso não Autorizado!</h3>", 401

