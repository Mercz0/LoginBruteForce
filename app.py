from flask import Flask, request, session, redirect, render_template
import json

app = Flask(__name__)
app.secret_key = 'clave_super_insegura'

def get_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def find_user(username):
    for user in get_users():
        if user['username'] == username:
            return user
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # VULNERABILIDAD: sin límite de intentos, sin bloqueo
        user = find_user(username)

        if user and user['password'] == password:
            session['user'] = user['username']
            return redirect('/dashboard')
        else:
            error = 'Credenciales incorrectas.'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)