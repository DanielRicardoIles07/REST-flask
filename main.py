from flask import Flask
from flask import jsonify
from flask import g
from flask import abort
from flask import request

from models import Empresa
from models import DATABASE

app = Flask(__name__) 
PORT = 4000 
DEBUG = True

@app.before_request 
def before_request():
    g.db = DATABASE
    g.db.connect()

@app.after_request 
def after_request(request):
    g.db.close()
    return request

@app.errorhandler(404)
def not_found(error):
    return jsonify(generate_response(404, error = 'not found Empresa'))

@app.errorhandler(400)
def bad_request(error):
    return jsonify(generate_response(400, error = 'you need params'))

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify(generate_response(422, error = 'Unprocessable Entity'))

@app.route('/apidataempresa/', methods =['GET'])
def get_datos():
    datos = Empresa.select()
    datos = [ empresa.to_json() for empresa in datos]
    return jsonify(generate_response(data = datos ))

@app.route('/apidataempresa/<int:id>', methods =['GET'])
def get_empresa(id):
    empresa = try_empresa(id)
    return jsonify(generate_response(data = empresa.to_json()))
            
def try_empresa(id):
    try:
        return Empresa.get(Empresa.id == id)
    except Empresa.DoesNotExist:
        abort(404)

def generate_response(status = 200, data = None, error = None):
    return {'status': status, 'data': data, 'error' : error}

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)