#Eigenentwicklung fügt zusätzliche kontextinformationen hinzu.
from app import app, db
from app.models import User, Server


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Server': Server}
