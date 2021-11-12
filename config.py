
class Config:
    EXTRA_AMOUNT = 12.12
    REDIRECT_URL = "http://meusite.com/obrigado"
    NOTIFICATION_URL = "http://meusite.com/notification"
    EMAIL = "madarah.impacta@gmail.com"
    TOKEN = "45B4AE1FB8684648B476ACA83627DA1D"
    SECRET_KEY = "s3cr3t"


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'


CONFIG = {
    'development': DevelopmentConfig
}