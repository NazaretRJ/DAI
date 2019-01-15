from flask import Flask

app = Flask(__name__)	#objeto de flash


@app.route('/') 	#se llama decorador y  .route es el enroutador y es para decir a url, si aparece esa url ejecuta la función que aparece 
def hello_world():	#abajo
    return '<head> <link rel="stylesheet" href="/static/estilos.css"></head><h2>HELLO WORLD</h2><p>Los usuarios definidos son:zerjillo,pepe,nazaret</p>' 

#esta funcion se ejecuta y devuelve hola mundo (aquí iría el html,porque no estamos usando aun MVC)

@app.route('/hola') #ahora si ponemos localhost:8080/hola te da este mensaje
def hello_world2():
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>HOLI</h2><img src=/static/rapunzel.jpg>'

@app.route('/user/<usuario>',methods=['GET'])
def cogerUsuario(usuario = None):
    if(usuario == None):
        return '<h3>¿Cómo te llamas?<h3>'
    else:
        if(usuario == 'zerjillo'):
           return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>Hola :)</h2><img src=/static/perrete.jpg>' 
        else:
            if(usuario == 'pepe'):
               return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>¡Hola Pepe!</h2>' 
            else:
                if(usuario == 'nazaret'):
                    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>¡Naza!</h2><img src=/static/rapunzel.jpg>'
                else:
                    return '<h1>Hola usuario :)</h1>'


@app.errorhandler(404) #pagina 404
def page_not_found(e):
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h1>Lo sentimos la página se ha perdido</h1> <img src=/static/lost.jpg>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar

#los objetos dinamicos tienen que ir en carpetas concretas
