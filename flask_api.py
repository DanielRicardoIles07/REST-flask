from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask import jsonify
from flask import g
from flask import abort
import pymysql

db = pymysql.connect("domiciliosurbanos.com", "joseluis", "597b9050653f3", "mu_domicilios")

app = Flask(__name__)

#database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restflask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init database
mysql = MySQL(app)

@app.route('/')
def Login():
	return render_template('login.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email  = StringField('Email', [validators.Length(min=4, max=50)])
    username = StringField('Username', [validators.Length(min=2, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
    	name = form.name.data
    	email = form.email.data
    	username = form.username.data
    	password = sha256_crypt.encrypt(str(form.password.data))

    	#create cursor
    	cur = mysql.connection.cursor()

    	cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))

    	#insertar en db
    	mysql.connection.commit()

    	#close conncection
    	cur.close()

    	flash('Register successfuly', 'success')

    	return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/api/puntos/domicilios/v.1.0')
def puntos():
    cursor = db.cursor()
    sql = "select p.id, p.nombre, empresa_id, p.lat, p.long, p.direccion, p.ciudad, (e.nombre) as empresa, e.mu_ref from puntos p left join empresa e on p.empresa_id = e.id where mu_ref is not null group by mu_ref order by ciudad"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results=results)

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
