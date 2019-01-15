from flask import Flask

app = Flask(__name__)	#objeto de flash


@app.route('/') 	#se llama decorador y  .route es el enroutador y es para decir a url, si aparece esa url ejecuta la función que aparece 
def hello_world():	#abajo
    return '<head> <link rel="stylesheet" href="/static/estilos.css"></head><h1>HELLO WORLD</h1> <img src=/static/rapunzel.jpg>' 

#esta funcion se ejecuta y devuelve hola mundo (aquí iría el html,porque no estamos usando aun MVC)

@app.route('/hola') #ahora si ponemos localhost:8080/hola te da este mensaje
def hello_world2():
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>HOLI</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar

#los objetos dinamicos tienen que ir en carpetas concretas
