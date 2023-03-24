#Eigenentwicklung, auf basis von Microblog. Importiert das Modul OS, sowie die Verzeichnise gesetzt und die Datenbankverbindung angegeben.
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

