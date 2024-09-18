from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,email,senha,nome="",tipo="") -> None:
        self.id = id
        self.email = email
        self.senha = senha
        self.nome = nome
        self.tipo = tipo
        self.remember =  False

    @classmethod
    def verify_password(self,hashed_password, senha):
        return check_password_hash(hashed_password,senha)
    
    @classmethod
    def create_password(self, senha):
        return generate_password_hash(senha, salt_length=16)