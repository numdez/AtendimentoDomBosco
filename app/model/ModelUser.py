from .entidades.Usuario import Usuario
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
                    row[3], user.senha), row[1], row[4], row[5])
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
            logged_user = Usuario(row[0], row[2], row[3],
                                row[1], row[4], row[5])
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