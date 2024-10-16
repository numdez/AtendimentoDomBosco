from app.model.ModelUser import ModelUser
from app.controller.auth import Auth
from app.utils import utils
from app.model import functions
from app.model.forms import LoginForm, AddAtendimentoForm
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
from datetime import timedelta, datetime
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
    current_user.atualiza_login()
    functions.loga_usuario(id_user)
    session['ultAbaAberta'] = 'home'
    usuario = utils.to_df(functions.get_usuario(id_user), 'usuario')
    return render_template('base.html')


@app.route('/chamado/add', methods=['GET', 'POST'])
def add_chamado():
    form = AddAtendimentoForm()

    if form.validate_on_submit():
        assinatura_base64 = request.form['assinaturaCanvasData']
        if assinatura_base64:
            assinatura_base64 = assinatura_base64.split(",")[1]
            assinatura_bytes = base64.b64decode(assinatura_base64)
            assinatura_io = BytesIO(assinatura_bytes)
            imagem_assinatura = Image.open(assinatura_io)
            assinatura_string = base64.b64encode(assinatura_io.getvalue()).decode('utf-8')
        else:
            assinatura_string = ''
        if assinatura_string:
            if current_user.tipo == 'Usuário':
                proc = f"""INSERT INTO tbl_undb_chamados(
                    data_atendimento, nome_aluno, data_nasc_aluno, serie_aluno, turma_aluno, nome_responsavel, 
                    parentesco_responsavel, email_responsavel, telefone_responsavel, celular_responsavel,
                    solicitado_por, questoes, aconselhamento, providencias, observacoes_finais, assinatura_responsavel
                ) VALUES """
            elif current_user.tipo == 'Administrador' or current_user.tipo == 'Atendente':
                proc = f"""INSERT INTO tbl_undb_chamados(
                    data_atendimento, nome_aluno, data_nasc_aluno, serie_aluno, turma_aluno, nome_responsavel, 
                    parentesco_responsavel, email_responsavel, telefone_responsavel, celular_responsavel,
                    solicitado_por, questoes, aconselhamento, providencias, observacoes_finais, assinatura_atendente
                ) VALUES """
            args = (datetime.today().date(), form.nome_aluno.data, form.nascimento_aluno.data,
                    form.serie_aluno.data, form.turma_aluno.data, form.nome_responsavel.data,
                    form.parentesco_responsavel.data, form.email_responsavel.data, 
                    form.telefone_responsavel.data, form.celular_responsavel.data, form.solicitado_por.data,
                    form.questoes.data, form.aconselhamento.data, form.providencias.data, 
                    form.observacoes_finais.data, assinatura_string
                )
        else:
            proc = f"""INSERT INTO tbl_undb_chamados(
                    data_atendimento, nome_aluno, data_nasc_aluno, serie_aluno, turma_aluno, nome_responsavel, 
                    parentesco_responsavel, email_responsavel, telefone_responsavel, celular_responsavel,
                    solicitado_por, questoes, aconselhamento, providencias, observacoes_finais
                ) VALUES """
            args = (datetime.today().date(), form.nome_aluno.data, form.nascimento_aluno.data,
                    form.serie_aluno.data, form.turma_aluno.data, form.nome_responsavel.data,
                    form.parentesco_responsavel.data, form.email_responsavel.data, 
                    form.telefone_responsavel.data, form.celular_responsavel.data, form.solicitado_por.data,
                    form.questoes.data, form.aconselhamento.data, form.providencias.data, 
                    form.observacoes_finais.data
                )
        id = functions.run_blank_query(proc, args)
        return redirect(url_for('home'))
        #return redirect(url_for('view_atendimento', id_atendimento=id))
    return render_template('chamados/add_chamado.html', form=form)

@app.route('/chamado/view/<id_chamado>', methods=["GET", "POST"])
def view_chamado(id_chamado):
    chamado = utils.to_df(functions.get_chamado(id_chamado), 'chamado')
    chamado = utils.limpaDatas(chamado)
    log_action(current_user.nome, 'VIEW', 'CHAMADO', id_chamado)
    if isinstance(chamado['assinatura_responsavel'][0], str):
        ass_responsavel = utils.b64_to_bytes(chamado['assinatura_responsavel'][0])
        ass_responsavel = base64.b64encode(ass_responsavel).decode('utf-8')
    else:
        ass_responsavel = ''
    if isinstance(chamado['assinatura_atendente'][0], str):
        ass_atendente = utils.b64_to_bytes(chamado['assinatura_atendente'][0])
        ass_atendente = base64.b64encode(ass_atendente).decode('utf-8')
    else:
        ass_atendente = ''
    return render_template('chamados/view_chamado.html', chamado=chamado, ass_responsavel=ass_responsavel, ass_atendente=ass_atendente)

@app.route('/view/chamados', methods=["GET", "POST"])
def all_chamados():
    chamados = utils.to_df(functions.get_all_chamados(), 'chamado')
    chamados = utils.limpaDatas(chamados)
    return render_template('atendimentos.html', df_atendimentos=chamados)


@app.route('/teste/<id_chamado>')
def teste(id_chamado):
    imagem = utils.bytes_to_img(functions.run_blank_get(f'SELECT assinatura_atendente FROM tbl_undb_chamados WHERE id_chamado = {id_chamado}')[0][0])
    image = Image.open(imagem)
    image.show()
    return redirect(url_for('home'))

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

