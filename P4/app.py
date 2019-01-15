from flask import Flask
from flask import render_template, request, session, redirect, url_for
from pickleshare import * #doc that is a db
from pymongo import MongoClient #database permanent
from bson.objectid import ObjectId

app = Flask(__name__)	#objeto de flash

app.secret_key = 'contraseñasecreta' #Clave secreta: Para poder crear la cookie y cifrar su contenido necesita una clave secreta. 

db = PickleShareDB('./db') #donde están los usuarios

connection = MongoClient('localhost', 27017)
dbMongo = connection.test

@app.route('/')
@app.route('/index.html')  
def index():
    list_url(('','home')) #si lo pongo peta cuando no estoy logeado
    return render_template('index.html') 


@app.route('/work.html') 	 
def work():
    list_url(('work.html','Work'))
    return render_template('work.html') 

@app.route('/login.html', methods = ['GET', 'POST']) 	 
def login():
    error=None
    u_mail = ""

    list_url(('login.html','Login'))
    if 'name' in session:
        u_mail = session['email']
        u_name = session['name']
        return render_template('info.html')
    elif request.method == 'POST':
        u_mail = request.form['email']
        u_pwd = request.form['pass']

    if u_mail in db:
        if u_pwd == db[u_mail]['pass']:
            session['email'] = u_mail
            session['name'] = db[u_mail]['name']
            return redirect('info.html')
            
    error='Usuario no existe'

    
    return render_template('login.html',error=error) 

@app.route('/log_out')
def log_out():
    session.pop('name', None)
    session.pop('email',None)
    return redirect(url_for('index'))


def list_url(direccion):
    if 'name' in session:
        if 'visited_url' in session:
            session['visited_url'] = [direccion] + session['visited_url']
        else:
            session['visited_url'] = [direccion]

        while len(session['visited_url']) > 3:
            session['visited_url'].pop()
        
@app.route('/sign_up.html', methods = ['GET', 'POST'])
def sign_up():
    error = None
    in_use = False

    if 'name' in session :
       return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']

        if email in db:
            error = 'The email is alredy in use'       

        else:
            u_pwd = request.form['pass']
            u_name = request.form['name']
            db[email] = dict()
            db[email]['name'] = u_name
            db[email]['pass'] = u_pwd
            session['email'] = email
            session['name'] = u_name
            return redirect(url_for('index'))

    return render_template('sign_up.html', error=error)

@app.route('/update_info.html', methods = ['GET', 'POST'])
def update_info():
    error = None
    
    list_url(('update_info.html','Update'))
    if not 'name' in session:
        return redirect(url_for('login'))

    elif request.method == 'POST':
        email = session['email']
        name = request.form['name']
        db[email]['name'] = name
        session['name'] = name
        return redirect(url_for('login'))

    return render_template('update_info.html', error=error)

@app.route('/info.html')
def info():
    list_url(('info.html','User'))
    return render_template('info.html')

@app.route('/buscar.html',methods=['GET','POST'])
def buscar():

    if(request.method == 'POST'):
        query = dbMongo.restaurants.find({"name" : request.form['Nom']})
        if query == None:
            query = "No encontrado"
        return render_template('buscar.html', result=query)
    else:
        query = dbMongo.restaurants.find().limit(15)
        if query == None:
            query = "Fallo"
        return render_template('buscar.html', result=query)

@app.route('/modificar.html/<id>',methods=['GET','POST'])
def modificar(id = None):
    if(request.method == 'GET'):
        return render_template('modificar.html', id_mod=id)
    else:
        up = { "name" : request.form['Nom']}
        res2 = dbMongo.restaurants.update( {"_id" : ObjectId(request.form['id'])} , {"$set": up} )
        if res2['n'] == 1:
            return render_template('buscar.html',aviso="Modificado")
        else:
            return render_template('buscar.html',aviso="Error al modificar")


@app.route('/borrar.html/<id>',methods=['GET'])
def borrar(id = None):

    #res = dbMongo.restaurants.find({"_id" : request.form['id']})
    requisito = {"justOne":True}
    res2 = dbMongo.restaurants.remove({"_id" : ObjectId(id)} )
    if res2['n'] == 1:
        return render_template('buscar.html',aviso="Borrado")
    else:
        return render_template('buscar.html',aviso="Error al borrar")

    

@app.errorhandler(404) #pagina 404
def page_not_found(e):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar
