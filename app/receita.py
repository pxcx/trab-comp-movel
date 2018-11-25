from flask import jsonify, request
from flask_pymongo import ObjectId

class Receita:
	# construtor
	def __init__(self, mongo):
		self.mongo = mongo

	# retorna lista de receitas
	def get_all(self):
		receitas = self.mongo.db.receita
		output = []
		for receita in receitas.find():
			output.append(self.format(receita))

		return jsonify({'result' : output})

	# retorna uma receita por id
	def get_by_id(self, id):
		receitas = self.mongo.db.receita

		output = 'Nenhuma receita encontrada'
		if receitas.count({'_id': ObjectId(id) }) >= 1:
			receita = receitas.find_one({'_id': ObjectId(id) })
			output = self.format(receita)

		return jsonify({'result' : output})
			
	# remove uma receita
	def delete(self, id):
		receitas = self.mongo.db.receita

		output = 'Nenhuma receita encontrada'
		if receitas.count({'_id': ObjectId(id) }) >= 1:
			result = receitas.delete_one({'_id': ObjectId(id)})
			output = str(result.deleted_count) + ' registro foi removido'
			
		return jsonify({'result' : output})

			
	# cadastra uma receita
	def add(self):
		receitas = self.mongo.db.receita

		descricao = request.json['descricao']
		data = request.json['data']
		usuario = ObjectId(request.json['user_id'])
		obs = request.json['obs']
		# imagens ??

		receita_id = receitas.insert({
			'descricao': descricao, 
			'data': data, 
			'usuario': usuario,
			'obs' : obs,
			'propostas': [], 
			'imagens': []
		})

		new = receitas.find_one({'_id': receita_id })
		return jsonify({'result' : self.format(new)})

	# funcao que formata a saida dos objetos
	def format(self, info):
		output = {
			'id' : str(info['_id']),
			'descricao' : info['descricao'], 
			'data' : info['data'], 
			'obs' : info['obs']
		}
		return output
