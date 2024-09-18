from .entidades.user import User


class ModelUser():
    def __init__(self):
        self._nome = 'pass'


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
            cursor.commit()
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