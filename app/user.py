from flask import jsonify, request
from flask_pymongo import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
	# construtor
	def __init__(self, mongo):
		self.mongo = mongo

	# retorna lista de usuarios
	def get_all(self):
		users = self.mongo.db.user
		output = []
		for user in users.find():
			output.append(self.format_user(user))

		return jsonify({'result' : output})

	# retorna um usuario por id
	def get_by_id(self, id):
		users = self.mongo.db.user

		output = 'Nenhum usuário encontrado'
		if users.count({'_id': ObjectId(id) }) >= 1:
			user = users.find_one({'_id': ObjectId(id) })
			output = self.format_user(user)

		return jsonify({'result' : output})
			
	# remove um usuario
	def delete(self, id):
		users = self.mongo.db.user

		output = 'Nenhum usuário encontrado'
		if users.count({'_id': ObjectId(id) }) >= 1:
			result = users.delete_one({'_id': ObjectId(id)})
			output = str(result.deleted_count) + ' registro foi removido'
			
		return jsonify({'result' : output})
			
	# autentica um usuario
	def login(self):
		users = self.mongo.db.user

		email = request.json['email']
		senha = request.json['senha']

		output = {'login': False, 'message': 'Combinação de usuário e senha incorreta.'}
		if users.count({'email': email}) >= 1:
			user = users.find_one({'email': email})
			if check_password_hash(user['senha'], senha):
				output = {'login': True, 'user': self.format_user(user)}
				
		return jsonify({'result' : output})
			
	# cadastra um usuario
	def add(self):
		users = self.mongo.db.user

		tipo = request.json['tipo']

		razao_social = request.json['razao_social']
		email = request.json['email']
		senha = generate_password_hash(request.json['senha'])
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
		return jsonify({'result' : self.format_user(new_user)})

	# funcao que formata a saida dos objetos
	def format_user(self, user):
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
