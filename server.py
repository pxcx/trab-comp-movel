from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.user import User
import urllib.parse

app = Flask('MyMedsAPI')
CORS(app)

app.config['MONGO_DBNAME'] = 'mymeds'
#app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/mymeds'
username = urllib.parse.quote_plus('heroku_t00ws3j1')
password = urllib.parse.quote_plus('ZSEfvcx@1425')
app.config['MONGO_URI'] = 'mongodb://%s:%s@ds147592.mlab.com:47592/heroku_t00ws3j1' % (username, password)
mongo = PyMongo(app)

# mensagem de erro padrao
def send_error(error):
	msg = str(error)
	print(type(error), type(error) is 'KeyError')
	if type(error) is KeyError:
		msg = 'O campo ' + str(error) + ' é obrigatório'
	return jsonify({'result' : 	'error' , 'reason': msg})

@app.route('/', methods=['GET'])
def index():
	return 'Ok!'

@app.route('/user', methods=['GET'])
def call_get_all_users():
	api = User(mongo)
	return api.get_all(), 200

@app.route('/user/<id>', methods=['GET'])
def call_get_user_by_id(id):
	api = User(mongo)
	return api.get_by_id(id), 200

@app.route('/user/<id>', methods=['DELETE'])
def call_delete_user(id):
	api = User(mongo)
	return api.delete(), 200

@app.route('/login', methods=['POST'])
def call_login_user():
	try:
		api = User(mongo)
		return api.login(), 200
	except Exception as e:
		return send_error(e), 500

@app.route('/user', methods=['POST'])
def call_add_user():
	api = User(mongo)
	return api.add()

#app.run(debug=True)