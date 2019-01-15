from django.shortcuts import render

# Create your views here.
from pickleshare import * #doc that is a db
from pymongo import MongoClient #database permanent

from django.shortcuts import render, HttpResponse
from .forms import BuscarRestaurante
from bson.objectid import ObjectId
from bson import json_util
import json
from django.http import JsonResponse

# Create your views here.
#app.secret_key = 'contraseñasecreta' #Clave secreta: Para poder crear la cookie y cifrar su contenido necesita una clave secreta. 

db = PickleShareDB('./db') #donde están los usuarios

connection = MongoClient('localhost', 27017)
dbMongo = connection.test
prev = 0
next = 0

def session_base(request):
    aux = None
    if 'name' in request.session:
        aux = request.session['name']
    context = {'sesion_name':aux}
    return context

def index(request):
    list_url(request,('','home'))
    context = session_base(request)
    return render(request,'index.html',context)

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)

from .models import restaurantes
from django.shortcuts import redirect
# ....
def test_template(request):
   iterador = restaurantes.find().limit(10)
   context = {
      "lista": list(iterador)
   }
   return render(request, 'test.html', context)

def work(request):
    list_url(request,('work.html','Work'))
    context = session_base(request)
    return render(request,'work.html',context) 
	 
def login(request):
    error=None
    u_mail = ""

    list_url(request,('login.html','Login'))
    if 'name' in request.session:
        u_mail = request.session['email']
        u_name = request.session['name']
        return render(request,'info.html')
    elif request.method == 'POST':
        u_mail = request.form['email']
        u_pwd = request.form['pass']

    if u_mail in db:
        if u_pwd == db[u_mail]['pass']:
            request.session['email'] = u_mail
            request.session['name'] = db[u_mail]['name']
            return redirect('info')
            
    error='Usuario no existe'
    
    aux = None
    if 'name' in request.session:
        aux = request.session['name']
    
    context={'error':error,'sesion_name':aux}
    
    return render(request,'login.html',context) 


def log_out(request):
    request.session.pop('name', None)
    request.session.pop('email',None)
    context = session_base(request)
    return redirect('index.html')


def list_url(request,direccion):
    if 'name' in request.session:
        if 'visited_url' in request.session:
            request.session['visited_url'] = [direccion] + request.session['visited_url']
        else:
            request.session['visited_url'] = [direccion]

        while len(request.session['visited_url']) > 3:
            request.session['visited_url'].pop()
        

def sign_up(request):
    error = None
    in_use = False

    if 'name' in request.session :
       return redirect('login.html')

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
            request.session['email'] = email
            request.session['name'] = u_name
            return redirect('index.html')
        context={'error': error}
    return render(request,'sign_up.html', context)


def update_info(request):
    error = None
    
    list_url(request,('update_info.html','Update'))
    if not 'name' in request.session:
        return redirect('login.html')

    elif request.method == 'POST':
        email = request.session['email']
        name = request.form['name']
        db[email]['name'] = name
        request.session['name'] = name
        return redirect('login.html')
    
    aux = None
    if 'name' in request.session:
        aux = request.session['name']
    
    context = {'error':error,'sesion_name':aux}
    
    return render(request,'update_info.html', context)


def info(request):
    list_url(request,('info.html','User'))
    return render(request,'info.html')


def buscar(request,pag=0):

    global prev
    global next
    aux = None
    tam = 10
    Max = 10

    context = {}
    #form = BuscarRestaurante()
    if 'name' in request.session:
        aux = request.session['name']

    if(request.method == 'POST'):
        # creamos una instancia con los datos del request
        buscar_res = BuscarRestaurante(request.POST)
        if buscar_res.is_valid():
            query = dbMongo.restaurants.find({"name" :buscar_res.cleaned_data.get('nombre')})
            #poner ObjectId
            
            if query == None:
                query = "No encontrado"
                context = {'result':query,'sesion_name':aux,'form':buscar_res,'prev':0,'next':0}
            else:
                context = {'result':query,'sesion_name':aux,'form':buscar_res,'prev':0,'next':0}
            return render(request,'buscar.html',context )
    else:
        try:
            aux = int(pag) * tam
        except TypeError:
            aux = 0

        buscar_res = BuscarRestaurante()
        query = dbMongo.restaurants.find()

        if(int(pag) ==  0):
            next = 1
            prev = -1
        else:
            prev = int(pag) - 1
            next = int(pag) + 1
        
        print(pag)
        print(prev)
        print(next)

        query.skip(aux)
        query.limit(Max)
        


        if query == None:
            query = "No hay más páginas"
            next = int(pag) -1
            prev = int(pag) - 2
        context = {'result':query,'sesion_name':aux,'form':buscar_res,'prev':prev,'next':next}
        return render(request,'buscar.html', context)



def modificar(request,id = None):
    aux = None
    if 'name' in request.session:
        aux = request.session['name']

    if(request.method == 'GET'):
        context = {'id_mod':id,'sesion_name':aux}
        return render(request,'modificar.html',context)
    else:
        up = { "name" : request.form['Nom']}
        res2 = dbMongo.restaurants.update( {"_id" : ObjectId(request.form['id'])} , {"$set": up} )
        if res2['n'] == 1:
            context = {'aviso':"Modificado",'sesion_name':aux}
            return render(request,'buscar.html',context)
        else:
            context = {'aviso':"Error al modificar",'sesion_name':aux}
            return render(request,'buscar.html',context)

def borrar(request,id = None):
    aux = None
    if 'name' in request.session:
        aux = request.session['name']
    #res = dbMongo.restaurants.find({"_id" : request.form['id']})
    requisito = {"justOne":True}
    res2 = dbMongo.restaurants.remove({"_id" : ObjectId(id)} )
    if res2['n'] == 1:
        context = {'aviso':"Borrado",'sesion_name':aux}
        return render(request,'buscar.html',context)
    else:
        context = {'aviso':"Error al borrar",'sesion_name':aux}
        return render(request,'buscar.html',context)

    
def buscar_ajax(request):
    return render(request,"buscar_ajax.html")

def getDatos(request):
    Max = 10
    pag = request.GET['pag']
    #print(pag)
    
    try:
        aux = int(pag) * Max
    except TypeError:
        aux = 0

    buscar_res = BuscarRestaurante()
    query = dbMongo.restaurants.find()

    query.skip(aux)
    query.limit(Max)
    #convierte en Json
    resp = json_util.dumps(query)
    print(resp)

        
    return JsonResponse(resp,safe=False)

#pagina 404
def page_not_found(e):
    return render('not_found.html')


