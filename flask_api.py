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

@app.route('/')
def Login():
	return render_template('login.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email  = StringField('Email', [validators.Length(min=4, max=20)])
    username = StringField('Username', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
    	return render_template('signup.html')
    return render_template('signup.html', form=form)


@app.route('/api/puntos/domicilios/v.1.0')
def puntos():
    cursor = db.cursor()
    sql = "select p.id, p.nombre, empresa_id, p.lat, p.long, p.direccion, p.ciudad, (e.nombre) as empresa, e.mu_ref from puntos p left join empresa e on p.empresa_id = e.id where mu_ref is not null group by mu_ref order by ciudad"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results=results)

if __name__ == '__main__':
	app.run(debug=True)
