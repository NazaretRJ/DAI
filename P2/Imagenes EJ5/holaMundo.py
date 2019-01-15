from flask import Flask
import random
from PIL import Image
import cv2

app = Flask(__name__)	#objeto de flash


@app.route('/hola') #ahora si ponemos localhost:8080/hola te da este mensaje
def hello_world2():
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h2>HOLI</h2><img src=/static/rapunzel.jpg>'

@app.route('/')
def Imagen():
    img = Image.new("RGB", (500, 500))
    a = 0
    if(a != 0):
        b = a + 1
        a = b
    # Crea una imagen en negro
    rn = random.randint(0,10)
    
    if rn > 5 :
        circulo(img)
    else:
        rectangulo(img)
    
    nombreFicheroPNG = "imagen"+str(a)
    img.save(nombreFicheroPNG, "PNG")
    


def circulo(img):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    pos_x = random.randint(0, 500)
    pos_y = random.randint(0, 500)

    rad = random.randint(0,300)

    cir = cv2.circle(img,(pos_x,pos_y),rad,(r,g,b), -1)


def rectangulo(img):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    pos_x = random.randint(0, 500)
    pos_y = random.randint(0, 500)

    lon = random.randint(10,100)

    rec = cv2.rectangle(img,(pos_x,pos_y),(pos_x+lon,pos_y+lon),(r,g,b),3)



@app.errorhandler(404) #pagina 404
def page_not_found(e):
    return '<head><link rel="stylesheet" href="/static/estilos.css"></head><h1>Lo sentimos la página se ha perdido</h1> <img src=/static/lost.jpg>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar

#los objetos dinamicos tienen que ir en carpetas concretas
