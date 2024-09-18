from app.model.ModelUser import ModelUser

def get_usuario(id):
    db = ModelUser()
    proc = f"SELECT * FROM tbl_undb_usuarios WHERE id_usuario = {id}"
    data = ModelUser.call_get_query(db, proc)
    return data