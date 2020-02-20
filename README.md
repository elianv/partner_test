...Las librerias estan en requirements.txt
...para levantar la API: python test.py

1. Create partner:
...url/partners
	...Datos para agregar deben ser enviados en el body del request, con metodo post

2. Get partner by id:
...url/partners/<id>
	...Donde el <id> es el id a buscar, debe ser enviado por metodo get

3. Search partner:
...url/partners/<lng>/<lat>
	...donde <lng> <lat> son las cordenadas donde se desea buscar el partner mas cercano, debe ser enviado por metodo get
