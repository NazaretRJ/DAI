from flask import Flask
from flask import render_template, request, session, redirect, url_for
from pickleshare import * #database

app = Flask(__name__)	#objeto de flash

app.secret_key = 'contraseñasecreta' #Clave secreta: Para poder crear la cookie y cifrar su contenido necesita una clave secreta. 

db = PickleShareDB('./db') #donde están los usuarios


#si no hago el clear,no fufa el pass cuando quito

@app.route('/')
@app.route('/index.html')  
def index():
    list_url(('','home'))
    return render_template('index.html') 


@app.route('/work.html') 	 
def work():
    list_url(('work.html','Work'))
    return render_template('work.html') 

@app.route('/login.html', methods = ['GET', 'POST']) 	 
def login():
    error=None
    u_mail = ""
    #try: 
    list_url(('login.html','Login'))
    if 'name' in session:
        u_mail = session['email']
        u_name = session['name']
        return render_template('info.html')
    elif request.method == 'POST':
        u_mail = request.form['email']
        u_pwd = request.form['pass']
    
    if u_mail != "":
        if u_mail in db:
            if u_pwd == db[u_mail]['pass']:
                session['email'] = u_mail
                session['name'] = db[u_mail]['name']
                return redirect('info.html')
        else:        
            error='Usuario o contraseña no existe'

    
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
        print(session['visited_url'])

@app.route('/sign_up.html', methods = ['GET', 'POST'])
def sign_up():
    error = None
    in_use = False

    #try:
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
            #para asegurarnos que pickleshare funciona
            #cuando hacemos una mod. en el diccionario, pickleshare, no se da cuenta
            #tenemos que poner esto:
            db[email] = db[email]

            return redirect(url_for('index'))
    #except:
    #    return redirect(url_for('log_out'))

    return render_template('sign_up.html', error=error)

@app.route('/update_info.html', methods = ['GET', 'POST'])
def update_info():
    error = None
    print('update')
    #try:
    list_url(('update_info.html','Update'))
    if not 'name' in session:
        return redirect(url_for('login'))

    elif request.method == 'POST':
        email = session['email']
        name = request.form['name']
        db[email]['name'] = name
        session['name'] = name
        db[email] = db[email]
        return redirect(url_for('login'))

    
    #except:
    #print('else') #quitar excepciones
    #return redirect(url_for('log_out'))

    return render_template('update_info.html', error=error)

@app.route('/info.html')
def info():
    list_url(('info.html','User'))
    return render_template('info.html')

@app.errorhandler(404) #pagina 404
def page_not_found(e):
    return render_template('not_found.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #0.0.0.0 escucha a todos los puertos de la maquina debug para desarrollar
