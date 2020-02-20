import json
import math
from flask import Flask, request
from flask_restful import Api
from flask.views import MethodView
from shapely.geometry import shape, Point
import jsonschema

app = Flask(__name__)
api = Api(app)


class Partners(MethodView):

	def getJson(self):
		file = open("pdvs.json", "r")
		contents = json.loads(file.read())
		file.close()
		return contents

	def wJson(self, data):
		file = open("pdvs.json", "w")
		file.write(json.dumps(data))
		file.close

	def JsonSchema(self, data):
		file = open("schema.json", "r")
		schema_data = json.loads(file.read())
		file.close()


		validationErrors = []
		v = jsonschema.Draft4Validator(schema_data)
		for error in v.iter_errors(data):
		    validationErrors.append(error)

		if len(validationErrors):
			return False, 'Error problemas con el JSON'

		return True, 'Validacion OK'

	def get(self, param1, param2=None):
		
		data = self.getJson()
		if param1 is not None and param2 is None:
			#Recorro todo los partners buscando aquel id que me dan.
			for i in data['pdvs']:
				if i['id'] == str(param1):
					return i
			return {'error': str(param1) +' id no encontrado'}

		elif param1 is not None and param2 is not None:
			point = Point(float(param1), float(param2))
			data = self.getJson()
			encontrado = None
			for i in data['pdvs']:
				app.logger.error(i)
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

		else:
			return {'error' : 'Hubo un problema con los parametros entregados.'}

	def post(self):
		data = self.getJson()
		request_json = json.loads(request.data)

		varOut, mensaje = self.JsonSchema(request_json)

		if not varOut:
			return {'Error' : mensaje}
		
		# agrego al final del json el elemento que me dan
		key = 0
		for i in data['pdvs']:
			if key < i['id']:
				last_key =  i['id']
				key = int(i['id']) + 1

		data['pdvs'].append(request_json)
		data['pdvs'][len(data['pdvs'])-1]['id'] = str(key)
		self.wJson(data)
		return {'code':'Insersion exitosa', 'id': str(key)}			


partnet_view = Partners.as_view('partners')
app.add_url_rule('/partners/', view_func=partnet_view, methods=['POST',])
app.add_url_rule('/partners/<int:param1>/',view_func=partnet_view, methods=['GET',])
app.add_url_rule('/partners/<param1>/<param2>',view_func=partnet_view, methods=['GET',])



#api.add_resource(Partners, '/partners/<id>')
#api.add_resource(Partners2, '/partners/<lng>/<lat>')
#api.add_resource(Partners3, '/partners')

if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)

