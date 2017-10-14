from flask import Flask, request, render_template
from flask import jsonify
from flask import g
from flask import abort
from flask import request
import pymysql

db = pymysql.connect("domiciliosurbanos.com", "joseluis", "597b9050653f3", "mu_domicilios")

app = Flask(__name__)

@app.route('/api/puntos/domicilios/v1.0')
def puntos():
    cursor = db.cursor()
    sql = "select p.id, p.nombre, empresa_id, p.lat, p.long, p.direccion, p.ciudad, (e.nombre) as empresa, e.mu_ref from puntos p left join empresa e on p.empresa_id = e.id where mu_ref is not null group by mu_ref order by ciudad"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results = results)

if __name__ == '__main__':
	app.run(debug=True)
