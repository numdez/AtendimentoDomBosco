from .entidades.Usuario import Usuario
import pandas as pd
import sqlite3


class ModelUser():
    def __init__(self):
        self._nome = 'app.db'
        self._conn = self._connecting()

    def _connecting(self):
        conn = sqlite3.connect(self._nome)
        return conn


    @classmethod
    def login(self, db, user):
        try:
            cursor = db._conn.cursor()
            sql = (
                f"SELECT * FROM tbl_undb_usuarios WHERE email_usuario = '{user.email}'")
            row = cursor.execute(sql).fetchone()
            if row != None:
                usuario = pd.DataFrame(
                    [row], 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
                if Usuario.verify_password(usuario['senha_usuario'][0], user.senha):
                    usuario = Usuario(usuario['id_usuario'][0], usuario['email_usuario'][0], usuario['senha_usuario'][0], 
                            usuario['nome_usuario'][0], usuario['tipo_usuario'][0], usuario['ult_data_login'][0])
                else:
                    usuario = 'Senha ou email inválido(s)!'
                db._conn.close()
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def auth_login(self, db, email):
        try:
            cursor = db._conn.cursor()
            sql = (
                f"SELECT * FROM tbl_undb_usuarios WHERE email_usuario = '{email}'")
            row = cursor.execute(sql).fetchone()
            if row != None:
                user = pd.DataFrame(
                    [row], 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
                user = Usuario(user['id_usuario'][0], user['email_usuario'][0], user['senha_usuario'][0], 
                            user['nome_usuario'][0], user['tipo_usuario'][0], user['ult_data_login'][0])
                db._conn.close()
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    


    @classmethod
    def get_by_id(self, db_loader, id):
        cursor = db_loader._conn.cursor()
        sql = (
            f'SELECT * FROM tbl_undb_usuarios WHERE id_usuario={id}'
        )
        
        row = cursor.execute(sql).fetchone()
        if row != None:
            logged_user = pd.DataFrame(
                    [row], 
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
            logged_user = Usuario(logged_user['id_usuario'][0], logged_user['email_usuario'][0], logged_user['senha_usuario'][0], 
                            logged_user['nome_usuario'][0], logged_user['tipo_usuario'][0], logged_user['ult_data_login'][0])
            return logged_user
        else:
            return None

    @classmethod
    def call_get_query(self, db, query):
        temp = []
        results = []
        try:
            cursor = db._conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                temp = [elem for elem in row]
                results.append(temp)
            db._conn.close()
            if results:
                return results
                print(results)
            else:
                return ''
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def call_set_query(self, db, query):
        try:
            cursor = db._conn.cursor()
            cursor.execute(query)
            db._conn.commit()
            db._conn.close()
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def call_bimethod_query(self, db, query):
        cursor = db._conn.cursor()
        cursor.execute(query)
        results = cursor.fetchone()[0]
        cursor.commit()
        db._conn.close()
        return results