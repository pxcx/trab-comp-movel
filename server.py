from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'mymeds'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mymeds'

mongo = PyMongo(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = mongo.db.user
    output = []
    for user in users.find():
        output.append(format_user(user))

    return jsonify({'result' : output})

@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    users = mongo.db.user

    output = 'Nenhum usuário encontrado'
    if users.count({'_id': ObjectId(id) }) >= 1:
        user = users.find_one({'_id': id })
        output = format_user(user)

    return jsonify({'result' : output})
        

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    users = mongo.db.user

    output = 'Nenhum usuário encontrado'
    if users.count({'_id': ObjectId(id) }) >= 1:
        result = users.delete_one({'_id': ObjectId(id)})
        output = str(result.deleted_count) + ' registro foi removido'
        
    return jsonify({'result' : output})
        

@app.route('/login', methods=['POST'])
def login_user(id):
    users = mongo.db.user

    email = request.json['email']
    senha = request.json['senha']

    output = 'Nenhum usuário encontrado'
    if users.count({'email': email, 'senha': senha }) >= 1:
        user = users.find_one({'_id': id })
        output = format_user(user)
        

@app.route('/user', methods=['POST'])
def add_user():
    users = mongo.db.user

    tipo = request.json['tipo']

    razao_social = request.json['razao_social']
    email = request.json['email']
    senha = request.json['senha']
    telefone = request.json['telefone']
    endereco_rua = request.json['endereco_rua']
    endereco_num = request.json['endereco_num']
    endereco_cep = request.json['endereco_cep']
    endereco_bairro = request.json['endereco_bairro']

    user_id = users.insert({
        'razao_social': razao_social, 
        'email': email, 
        'senha': senha,
        'telefone' : telefone,
        'endereco_rua': endereco_rua, 
		'endereco_num': endereco_num, 
		'endereco_cep': endereco_cep, 
        'endereco_bairro': endereco_bairro, 
        'tipo': tipo
    })

    new_user = users.find_one({'_id': user_id })
    return jsonify({'result' : format_user(new_user)})

# funcao que formata a saida dos objetos
def format_user(user):
	output = {
        'id' : str(user['_id']),
        'razao_social' : user['razao_social'], 
        'email' : user['email'], 
        'senha' : user['senha'], 
        'telefone' : user['telefone'], 
        'endereco_rua' : user['endereco_rua'], 
        'endereco_num' : user['endereco_num'], 
        'endereco_cep' : user['endereco_cep'],
		'endereco_bairro' : user['endereco_bairro'], 
		'tipo' : user['tipo']
    }
	return output

if __name__ == '__main__':
    app.run(debug=True)
