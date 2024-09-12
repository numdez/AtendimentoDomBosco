from datetime import timedelta
import os
class Config():
    SECRET_KEY=''
    
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
    MAIL_SERVER = 'email-ssl.com.br'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = f''
    MAIL_DEFAULT_SENDER = ''
    WTF_CSRF_TIME_LIMIT = 7200


config={
    'development':Config
}