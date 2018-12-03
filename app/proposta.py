from flask import jsonify, request, url_for
from werkzeug.utils import secure_filename
from flask_pymongo import ObjectId
import os

class Proposta:
	# construtor
	def __init__(self, mongo):
		self.mongo = mongo

	# retorna a lista de propostas por id de receita
	def get(self, receita):
		propostas = self.mongo.db.proposta

		output = []
		if propostas.count({'receita': ObjectId(receita) }) >= 1:
			for proposta in propostas.find({'receita': ObjectId(receita)}):
				output.append(self.format(proposta))

		return jsonify({'result' : output})
			
	# remove uma proposta
	def delete(self, id):
		propostas = self.mongo.db.proposta

		output = 'Nenhuma proposta encontrada'
		if propostas.count({'_id': ObjectId(id) }) >= 1:
			result = propostas.delete_one({'_id': ObjectId(id)})
			output = str(result.deleted_count) + ' registro foi removido'
			
		return jsonify({'result' : output})

			
	# cadastra uma proposta
	def add(self):
		propostas = self.mongo.db.proposta

		valor = float(request.json['valor'])
		entrega = float(request.json['entrega'])
		receita = ObjectId(request.json['receita_id'])
		obs = request.json['obs']

		receita_id = propostas.insert({
			'valor': format(valor, '.2f'), 
			'entrega': format(entrega, '.2f'), 
			'receita': receita,
			'obs' : obs
		})

		new = propostas.find_one({'_id': receita_id })
		return jsonify({'result' : self.format(new)})

	# funcao que formata a saida dos objetos
	def format(self, info):
		output = {
			'id' : str(info['_id']),
			'receita' : str(info['receita']),
			'entrega' : info['entrega'], 
			'valor' : info['valor'], 
			'obs' : info['obs']
		}
		return output
