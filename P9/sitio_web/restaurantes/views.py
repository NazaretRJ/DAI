from django.shortcuts import render

# Create your views here.
from pickleshare import * #doc that is a db
from pymongo import MongoClient #database permanent

from django.shortcuts import render, HttpResponse
from .forms import BuscarRestaurante
from bson.objectid import ObjectId

from osmapi import OsmApi

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
MapAppy = OsmApi()

def session_base(request):
    aux = None
    if 'name' in request.session:
        aux = request.session['name']
    context = {'sesion_name':aux}
    return context

def index(request):
    list_url(request,('','home'))

    return render(request,'index.html')

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
    
    return render(request,'work.html') 
	 


def list_url(request,direccion):
    if 'name' in request.session:
        if 'visited_url' in request.session:
            request.session['visited_url'] = [direccion] + request.session['visited_url']
        else:
            request.session['visited_url'] = [direccion]

        while len(request.session['visited_url']) > 3:
            request.session['visited_url'].pop()
        




def buscar(request,pag=0):

    global prev
    global next
    aux = None
    tam = 10
    Max = 10

    context = {}
    #form = BuscarRestaurante()


    if(request.method == 'POST'):
        # creamos una instancia con los datos del request
        buscar_res = BuscarRestaurante(request.POST)
        if buscar_res.is_valid():
            query = dbMongo.restaurants.find({"name" :buscar_res.cleaned_data.get('nombre')})
            #poner ObjectId
            
            if query == None:
                query = "No encontrado"

            context = {'result':query,'sesion_name':aux,'form':buscar_res,'prev':0,'next':0,'post':True}
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

        query.skip(aux)
        query.limit(Max)
        
        if query == None:
            query = "No hay más páginas"
            next = int(pag) -1
            prev = int(pag) - 2
        context = {'result':query,'sesion_name':aux,'form':buscar_res,'prev':prev,'next':next,'post':False}
        return render(request,'buscar.html', context)



def modificar(request,id = None):
    aux = None


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

    #res = dbMongo.restaurants.find({"_id" : request.form['id']})
    requisito = {"justOne":True}
    res2 = dbMongo.restaurants.remove({"_id" : ObjectId(id)} )
    if res2['n'] == 1:
        context = {'aviso':"Borrado",'sesion_name':aux}
        return render(request,'buscar.html',context)
    else:
        context = {'aviso':"Error al borrar",'sesion_name':aux}
        return render(request,'buscar.html',context)


def buscar_mapa(request,nombre_res=None):
    
    buscar_res = BuscarRestaurante()
    print(nombre_res)
    #if buscar_res.is_valid():
    query = dbMongo.restaurants.find_one({"name" :nombre_res})
    
    if query != None:
        #Debemos crear un nodo con el resultado y mostrarlo
        coord = query['location']['coordinates']
        #print(coord)
        context = {
            'map_lat' : coord[0],
            'map_lon': coord[1],
        }
        
        #context = {'nodo_mapa':nodo_aux}
        return render(request,'mapa.html',context)
    else:
        return render(request,'not_found.html')
    #else:
    #    return render(request,'not_found.html')

def grafico(request):
    return render(request,'grafico.html')

def grafico_ajax(request):
    return render(request,"grafico_ajax.html")

def modDatosGraf(request):
    rest = request.GET['rest']
    plat = request.GET['platos']
    data = {'rest':rest,'platos':plat}
    
    resp = json_util.dumps(data)
    print(resp)

        
    return JsonResponse(resp,safe=False)

#pagina 404
def page_not_found(e):
    return render(e,'not_found.html')


