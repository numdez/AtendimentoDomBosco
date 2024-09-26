from app.model.ModelUser import ModelUser

def get_all_chamados():
    db = ModelUser()
    proc = f"SELECT * FROM tbl_undb_chamados"
    data = ModelUser.call_get_query(db, proc)
    return data

def get_usuario(id):
    db = ModelUser()
    proc = f"SELECT * FROM tbl_undb_usuarios WHERE id_usuario = {id}"
    data = ModelUser.call_get_query(db, proc)
    return data

def get_chamado(id):
    db = ModelUser()
    proc = f"SELECT * FROM tbl_undb_chamados WHERE id_chamado = {id}"
    data = ModelUser.call_get_query(db, proc)
    return data

def get_chamados_usuario(id):
    db = ModelUser()
    proc = f"SELECT * FROM tbl_undb_chamados WHERE id_usuario = {id}"
    data = ModelUser.call_get_query(db, proc)
    return data

