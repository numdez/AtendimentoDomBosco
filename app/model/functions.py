from app.model.ModelUser import ModelUser
from datetime import datetime

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

def loga_usuario(id):
    db = ModelUser()
    dataAtual = datetime.today().date()
    proc = f"UPDATE tbl_undb_usuarios SET ult_data_login = '{dataAtual}' WHERE id_usuario = {id}"
    ModelUser.call_set_query(db, proc)

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

def set_new_atendimento(args):
    db = ModelUser()
    proc = f"""INSERT INTO tbl_undb_chamados(
        data_atendimento, nome_aluno, data_nasc_aluno, serie_aluno, turma_aluno, nome_responsavel, 
        parentesco_responsavel, email_responsavel, telefone_responsavel, celular_responsavel,
        solicitado_por, questoes, aconselhamento, providencias, observacoes_finais
    ) VALUES """ + args
    data = ModelUser.call_bimethod_query(db, proc)
    return data