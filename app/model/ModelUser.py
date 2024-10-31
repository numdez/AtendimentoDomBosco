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
                user = Usuario(row[0], row[2], Usuario.verify_password(
                    row[3], user.senha), row[1], row[7], row[6])
                db._conn.close()
                return user
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
                    columns=['id_usuario', 'nome_usuario', 'email_usuario', 'senha_usuario', 'external_login', 
                        'auth_secret', 'ult_data_login', 'tipo_usuario', 'assinatura']
                )
                user = Usuario(user['id_usuario'][0], user['email_usuario'][0], user['senha_usuario'][0], 
                            user['nome_usuario'][0], user['tipo_usuario'][0], user['ult_data_login'][0],
                            user['external_login'][0], user['auth_secret'][0])
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
            logged_user = Usuario(row[0], row[2], row[3], row[1], row[7], row[6])
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