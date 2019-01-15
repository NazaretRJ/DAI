from django.shortcuts import render

# Create your views here.

from pymongo import MongoClient #database permanent

from django.shortcuts import render, HttpResponse
from .forms import BuscarRestaurante
from bson.objectid import ObjectId

from .models import restaurantes
from django.shortcuts import redirect

from .models import *
from .forms import *

from allauth.account.views import SignupView, LoginView


class MySignupView(SignupView):
    template_name = 'sing_up.html'


class MyLoginView(LoginView):
    template_name = 'login.html'

# Create your views here.
#app.secret_key = 'contraseñasecreta' #Clave secreta: Para poder crear la cookie y cifrar su contenido necesita una clave secreta. 


connection = MongoClient('localhost', 27017)
dbMongo = connection.test

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
    
    return render(request,'login.html') 


def log_out(request):

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

    return render(request,'sign_up.html')


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

def buscar(request):
    aux = None
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
            context = {'result':query,'sesion_name':aux,'form':buscar_res}
        
            return render(request,'buscar.html',context )
    else:
        buscar_res = BuscarRestaurante()
        query = dbMongo.restaurants.find().limit(15)
        print(query)
        if query == None:
            query = "Fallo"
        context = {'result':query,'sesion_name':aux,'form':buscar_res}
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


def buscar_plato(request):

    aux = None
    context = {}
    #form = BuscarRestaurante()
    if 'name' in request.session:
        aux = request.session['name']
    borrar_res = BorrarPlato(request.POST)
    if(request.method == 'POST'):
        print("aqui")
        buscar_res = BuscarPlato(request.POST)
        if(buscar_res.is_valid()):
            name_pla = buscar_res.cleaned_data['nombre']
            query = Platos.objects.filter(name=name_pla)

            if(query != None):
                context = {'result':query,'sesion_name':aux,'form':buscar_res,'form_borrar':borrar_res}
            else:
                context = {'aviso':"No encontrado",'sesion_name':aux,'form':buscar_res,'form_borrar':borrar_res}
        
            return render(request,'buscar_plato.html',context )
        # buscamos     
    else:
        buscar_res = BuscarPlato(request.POST)
        print("get")
        query = Platos.objects.all()
        if(query != None):
            context = {'result':query,'sesion_name':aux,'form':buscar_res,'form_borrar':borrar_res}
        else:
            context = {'aviso':"No encontrado",'sesion_name':aux,'form':buscar_res,'form_borrar':borrar_res}
        
        return render(request,'buscar_plato.html',context)

def borrar_plato(request):

    aux = None
    context = {}
    #form = BuscarRestaurante()
    if 'name' in request.session:
        aux = request.session['name']
    buscar_form = BuscarPlato(request.POST)
    if(request.method == 'POST'):
        print("aqui")
        borrar_res = BorrarPlato(request.POST)
        if(borrar_res.is_valid()):
            name_pla = borrar_res.cleaned_data['nombre_borrar']
            query = Platos.objects.filter(name=name_pla).delete()
            #query.save()
            if(query != None):
                context = {'result':"Borrado",'sesion_name':aux,'form':buscar_form,'form_borrar':borrar_res}
            else:
                context = {'aviso':"No encontrado",'sesion_name':aux,'form':buscar_form,'form_borrar':borrar_res}
        
        return render(request,'buscar_plato.html',context )
       
    


#pagina 404
def page_not_found(e):
    return render('not_found.html')


