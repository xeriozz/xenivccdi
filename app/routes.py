#Eigenentwicklung: Importiert die verschiedene Module und Funktionien.
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required
from app import app, db
from werkzeug.security import generate_password_hash
from app.models import User, Server


#Eigenentwicklung: Flask-Route für die Registrierung eines neuen Benutzers
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already taken. Please choose another username.'
            return render_template('signup.html', error=error)
        

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            error = 'Email already taken. Please choose another email.'
            return render_template('signup.html', error=error)
        

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


#Eigenentwicklung: Flask-Route für die Anmeldung eines Benutzers
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid username or password')
            return redirect(url_for('login'))


        if not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))


        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

#Eigenentwicklung: Flask-Route für die Abmeldung
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Eigenentwicklung: Flask-Route für die Hauptseite der Anwendung, mit Hinzufügen und Suchen neuer Einträge
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search_term = request.form.get('search_term', '')
    
    if request.method == 'POST':
        form_data = request.form.to_dict()
        servername = form_data.get('servername')
        ip = form_data.get('ip')
        os = form_data.get('os')


        if not all((servername, ip, os)):
            error_message = "all fields are reqiured"
            servers = Server.query.all()
            return render_template('index.html', error=error_message, servers=servers, search_term=search_term)


        existing_server = Server.query.filter_by(servername=servername).first()
        existing_ip = Server.query.filter_by(ip=ip).first()
        
        if existing_server is not None:
            error_message = f"server name '{servername}' is already in use"
            servers = Server.query.all()
            return render_template('index.html', servers=servers, error=error_message)

        if existing_ip is not None:
            error_message = f"IP address '{ip}' is already in use"
            servers = Server.query.all()
            return render_template('index.html', servers=servers, error=error_message)

        server = Server(servername=servername, ip=ip, os=os)
        db.session.add(server)
        db.session.commit()
        flash('server added successfully')
        return redirect(url_for('index'))

    else:
        search_term = request.args.get('search_term', '')
        if search_term:
            servers = Server.query.filter((Server.servername.like(f'%{search_term}%')) | (Server.ip.like(f'%{search_term}%')) | (Server.os.like(f'%{search_term}%'))).all()
            if not servers:
                error_message = (f"no servers found matching '{search_term}'. showing all servers instead.")
                servers = Server.query.all()
                return render_template('index.html', servers=servers, error=error_message)
        else:
            servers = Server.query.all()
        return render_template('index.html', servers=servers, search_term=search_term)


#Eigenentwicklung: Flask-Route für die Editierung eines bestähenden Eintrags.

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    server = Server.query.get_or_404(id)

    if request.method == 'POST':
        form_data = request.form.to_dict()
        servername = form_data.get('servername')
        ip = form_data.get('ip')
        os = form_data.get('os')

        if not all((servername, ip, os)):
            error_message = "all fields are reqiured"
            return render_template('edit.html', server=server, error=error_message)

        existing_server = Server.query.filter(Server.id != id, Server.servername == servername).first()
        existing_ip = Server.query.filter(Server.id != id, Server.ip == ip).first()

        if existing_server is not None:
            error_message = f"server name '{servername}' is already in use"
            return render_template('edit.html', server=server, error=error_message)

        if existing_ip is not None:
            error_message = f"IP address '{ip}' is already in use"
            return render_template('edit.html', server=server, error=error_message)

        server.servername = servername
        server.ip = ip
        server.os = os
        db.session.commit()
        flash('server updated successfully')
        return redirect(url_for('index'))

    return render_template('edit.html', server=server)

#Eigenentwicklung: Flask-Route für die Löschung eines Eintrags

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    server = Server.query.get_or_404(id)
    db.session.delete(server)
    db.session.commit()
    flash('server deleted successfully')
    return redirect(url_for('index'))

#Eigenentwicklung: Flask-Route, die eine JSON-Liste von allen Servern aus der Datenbank zurückgibt.
@app.route('/api/serverlist', methods=['GET'])
def api_serverlist():
    serverlist = Server.query.all()
    return jsonify([i.serialize() for i in serverlist])