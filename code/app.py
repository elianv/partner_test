import json
import math
from flask import Flask, request
from flask_restful import Resource, Api
from shapely.geometry import shape, Point

app = Flask(__name__)
api = Api(app)


def getJson():
	file = open("pdvs.json", "r")
	contents = json.loads(file.read())
	file.close()
	return contents

def wJson(data):
	file = open("pdvs.json", "w")
	file.write(json.dumps(data))
	file.close

class Partners(Resource):

	def get(self, id):
		data = getJson()
		#Recorro todo los partners buscando aquel id que me dan.
		for i in data['pdvs']:
			if i['id'] == str(id):
				return i

class Partners2(Resource):
		
	def get(self, lng, lat):
		point = Point(float(lng), float(lat))
		data = getJson()
		encontrado = None
		for i in data['pdvs']:
			poligonos = i['coverageArea']
			polygon = shape(poligonos)
			if polygon.contains(point):
				distancia = math.sqrt((float(lng)-float(i['address']['coordinates'][0]))**2+(float(lat)-float(i['address']['coordinates'][1]))**2)
				dist_a = distancia
				if distancia < dist_a:
					encontrado = i

		if encontrado is not None:
			return encontrado
		else:
			return {'error':'No se encontro punto mas cercano'}


class Partners3(Resource):

	def post(self):
		data = getJson()
		json_data = json.loads(request.data)
		# aqui deberia validar la data con el standar del json 
		# agrego al final del json el elemento que me dan
		key = 0
		for i in data['pdvs']:
			if key < i['id']:
				last_key =  i['id']
				key = int(i['id']) + 1

		data['pdvs'].append(json_data)
		data['pdvs'][len(data['pdvs'])-1]['id'] = str(key)
		wJson(data)
		return {'code':'Insersion exitosa', 'id': str(key)}

api.add_resource(Partners, '/partners/<id>')
api.add_resource(Partners2, '/partners/<lng>/<lat>')
api.add_resource(Partners3, '/partners')

if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)

