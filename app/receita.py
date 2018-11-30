from flask import jsonify, request, url_for
from werkzeug.utils import secure_filename
from flask_pymongo import ObjectId
import os

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

	# retorna uma receita por id de usuario
	def get_by_user(self, user):
		receitas = self.mongo.db.receita

		output = 'Nenhuma receita encontrada pra este usuário'
		if receitas.count({'usuario': ObjectId(user) }) >= 1:
			receita = receitas.find_one({'usuario': ObjectId(user) })
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

		descricao = request.form['descricao']
		data = request.form['data']
		usuario = ObjectId(request.form['user_id'])
		obs = request.form['obs']
		# imagem
		upload = request.files['receita']
		if upload:
			filename = secure_filename(upload.filename)
			upload.save(os.path.join('./files/', filename))
			imagem = request.base_url.replace('receita','')+'files/'+filename
		else:
			imagem = False

		receita_id = receitas.insert({
			'descricao': descricao, 
			'data': data, 
			'usuario': usuario,
			'obs' : obs,
			'propostas': [], 
			'receita': imagem
		})

		new = receitas.find_one({'_id': receita_id })
		return jsonify({'result' : self.format(new)})

	# funcao que formata a saida dos objetos
	def format(self, info):
		output = {
			'id' : str(info['_id']),
			'descricao' : info['descricao'], 
			'data' : info['data'], 
			'obs' : info['obs'],
			'receita' : info['receita']
			'usuario' : str(info['usuario'])
		}
		return output
