from flask import Flask,request

import mandelbrot

app = Flask(__name__)	#objeto de flash

#valores interesantes

# x1: -1.0
# y1: -1.0
# x2: 1.0
# y2: 1.0
# ancho: 300
# iteraciones: 100

@app.route('/')
def defecto():
    return '<h2>Ponga el nombre de fichero (nombre) y una de estas opciones (num) x1, y1, x2, y2, ancho).Ejemplo: nombre?=imagen1 & num?=1 </h2><p> 1 :-1.0,-1.0,1.0,1.0,300,100</p><p>2: -0.5,-0.5,0.5,0.5,250,75</p> <p>3: 0.5,0.5,-0.5,-0.5,250,75</p>'

@app.route('/<int:num>/')
def generarmandelbrot(num):
    #num = request.args.get('num')
    #f = nombre
    #if(f == None):
    f = "./static/nombreDefault.png"
    #else:
     #   f = "./static/"+str(f)+".png"
    if(num != None):
        if(num == 1):
            mandelbrot.renderizaMandelbrot(float(-1.0),float(-1.0),float(1.0),float(1.0),int(300),int(100),str(f))
        elif (num == 2):
            mandelbrot.renderizaMandelbrot(float(-0.5),float(-0.5),float(0.5),float(0.5),int(250),int(75),str(f))
        else:
            mandelbrot.renderizaMandelbrot(float(0.5),float(1.0),float(-0.5),float(-1.0),int(300),int(100),str(f))

        return '<img src="/static/nombreDefault.png">'

@app.errorhandler(404) #pagina 404
def page_not_found(e):
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h1>Lo sentimos la página se ha perdido</h1> <img src=/static/lost.jpg>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar

#los objetos dinamicos tienen que ir en carpetas concretas
