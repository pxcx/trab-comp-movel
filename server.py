from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.user import User
from app.receita import Receita
from app.proposta import Proposta
import urllib.parse

app = Flask('MyMedsAPI')
CORS(app)

# MONGODB LOCAL
# app.config['MONGO_DBNAME'] = 'mymeds'
# app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/mymeds'
# MLAB
username = urllib.parse.quote_plus('pxcx')
password = urllib.parse.quote_plus('ci1425')
app.config['MONGO_URI'] = 'mongodb://%s:%s@ds147592.mlab.com:47592/heroku_t00ws3j1' % (username, password)

mongo = PyMongo(app)

# mensagem de erro padrao
def send_error(error):
	msg = str(error)
	if type(error) is KeyError:
		msg = 'O campo ' + str(error) + ' é obrigatório'
	return jsonify({'result' : 	'error' , 'reason': msg})

@app.route('/', methods=['GET'])
def index():
	return 'API Ok!'

# rotas usuario
@app.route('/user', methods=['GET'])
def call_get_all_users():
	try:
		api = User(mongo)
		return api.get_all(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/user/<id>', methods=['GET'])
def call_get_user_by_id(id):
	try:
		api = User(mongo)
		return api.get_by_id(id), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/user/<id>', methods=['DELETE'])
def call_delete_user(id):
	try:
		api = User(mongo)
		return api.delete(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/login', methods=['POST'])
def call_login_user():
	try:
		api = User(mongo)
		return api.login(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/user', methods=['POST'])
def call_add_user():
	try:
		api = User(mongo)
		return api.add()
	except Exception as e:
		return send_error(e), 500

# rotas receita
@app.route('/receita', methods=['GET'])
def call_get_all_receitas():
	try:
		api = Receita(mongo)
		return api.get_all(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/receita/user/<user>', methods=['GET'])
def call_get_receita_by_user(user):
	try:
		api = Receita(mongo)
		return api.get_by_user(user), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/receita/<id>', methods=['GET'])
def call_get_receita_by_id(id):
	try:
		api = Receita(mongo)
		return api.get_by_id(id), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/receita/<id>', methods=['DELETE'])
def call_delete_receita(id):
	try:
		api = Receita(mongo)
		return api.delete(id), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/receita', methods=['POST'])
def call_add_receita():
	try:
		api = Receita(mongo)
		return api.add(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/proposta/<receita>', methods=['GET'])
def call_get_proposta(receita):
	try:
		api = Proposta(mongo)
		return api.get(receita), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/proposta/<id>', methods=['DELETE'])
def call_delete_proposta(id):
	try:
		api = Proposta(mongo)
		return api.delete(id), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/proposta', methods=['POST'])
def call_add_proposta():
	try:
		api = Proposta(mongo)
		return api.add(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/files/<filename>')
def uploaded_file(filename):
	return send_from_directory('files/', filename)

#app.run(debug=True)