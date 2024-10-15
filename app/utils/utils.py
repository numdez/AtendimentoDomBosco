import pandas as pd
from io import BytesIO
from flask_login import current_user
from flask import redirect, url_for, abort, jsonify
from app.model import functions
from time import sleep
import base64

def to_df(data, tabela):
    if data:
        match tabela.lower():
            case 'usuario':
                data = pd.DataFrame(
                    data, 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'external_login', 
                        'auth_secret', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
            case 'chamado':
                data = pd.DataFrame(
                    data, 
                    columns=['id_chamado', 'data_atendimento', 'nome_aluno', 'data_nasc_aluno',
                        'serie_aluno', 'turma_aluno', 'nome_responsavel', 'parentesco_responsavel',
                        'email_responsavel', 'telefone_responsavel', 'celular_responsavel', 'solicitado_por',
                        'questoes', 'aconselhamento', 'providencias', 'observacoes_finais', 
                        'assinatura_responsavel', 'assinatura_atendente']
                )
    else:
        match tabela.lower():
            case 'usuario':
                data = pd.DataFrame( 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'external_login', 
                             'auth_secret', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
            case 'chamado':
                data = pd.DataFrame(
                    columns=['id_chamado', 'data_atendimento', 'nome_aluno', 'data_nasc_aluno',
                        'serie_aluno', 'turma_aluno', 'nome_responsavel', 'parentesco_responsavel',
                        'email_responsavel', 'telefone_responsavel', 'celular_responsavel', 'solicitado_por',
                        'questoes', 'aconselhamento', 'providencias', 'observacoes_finais', 'assinatura_responsavel', 'assinatura_atendente']
                )
    return data

def bytes_to_img(b64String):
    imageBytes = base64.b64decode(b64String)
    image_stream = BytesIO(imageBytes)
    return image_stream

def b64_to_bytes(b64String):
    imageBytes = base64.b64decode(b64String)
    return imageBytes