import pandas as pd
from io import BytesIO
from flask_login import current_user
from flask import redirect, url_for, abort, jsonify
from app.model import functions
from time import sleep


def to_df(data, tabela):
    if data:
        match tabela.lower():
            case 'usuario':
                data = pd.DataFrame(
                    data, 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'external_login', 'auth_secret', 'ult_data_login', 'tipo_usuario']
                )
    else:
        match tabela.lower():
            case 'usuario':
                data = pd.DataFrame( 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'external_login', 'auth_secret', 'ult_data_login', 'tipo_usuario']
                )
    return data