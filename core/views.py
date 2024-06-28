from django.shortcuts import render,redirect
from .models import *
from .forms import *
from random import choice
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,permission_required
from rest_framework import viewsets
from .serializers import *
from rest_framework.renderers import JSONRenderer
import requests
from django.core.paginator import Paginator

#API metodos de listar
def noticiasapi(request):
    try:
        # Obtener noticias desde tu propia API (ejemplo)
        response_noticias = requests.get('http://127.0.0.1:8000/api/noticias/')
        response_noticias.raise_for_status()  # Lanza excepción para errores HTTP
        noticias = response_noticias.json()

        ciudad = 'Santiago'  # Puedes cambiar la ciudad a la que desees
        url = f'https://wttr.in/{ciudad}?format=j1'
        response_clima = requests.get(url)

        # Obtener valores desde la API de Mindicador
        response_mindicador = requests.get('https://www.mindicador.cl/api')
        response_mindicador.raise_for_status()  # Lanza una excepción para errores HTTP
        valores = response_mindicador.json()

        uf = valores['uf']['valor']  # Valor de la UF
        dolar = valores['dolar']['valor']  # Valor del dólar
        euro = valores['euro']['valor']  # Valor del euro

        aux = {
            'lista': noticias,
            'uf': uf,
            'dolar': dolar,
            'euro': euro,
        }

        if response_clima.status_code == 200:
            datos_clima = response_clima.json()
            clima = {
                'ciudad': ciudad,
                'temperatura': datos_clima['current_condition'][0]['temp_C'],
                'descripcion': datos_clima['current_condition'][0]['weatherDesc'][0]['value'],
                'humedad': datos_clima['current_condition'][0]['humidity'],
                'viento': datos_clima['current_condition'][0]['windspeedKmph']
            }
        else:
            clima = None

        aux['clima'] = clima

    except requests.exceptions.RequestException as e:
        # Manejar cualquier error de solicitud
        print(f"Error al obtener datos de la API: {e}")
        aux = {
            'lista': [],
            'uf': None,
            'dolar': None,
            'euro': None,
            'clima': None,
        }

    return render(request, 'core/Noticias/crudapi/index.html', aux)



def noticiadetalle(request,id):
    response=requests.get(f'http://127.0.0.1:8000/api/noticias/{id}/')
    noticias = response.json()
    aux = {
        'noticia' : noticias
    }
    return render(request, 'core/Noticias/crudapi/detalle.html', aux)


def climaapi(request):
    ciudad = 'Santiago'  # Puedes cambiar la ciudad a la que desees
    url = f'https://wttr.in/{ciudad}?format=j1'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        datos_clima = response.json()
        
        clima = {
            'ciudad': ciudad,
            'temperatura': datos_clima['current_condition'][0]['temp_C'],
            'descripcion': datos_clima['current_condition'][0]['weatherDesc'][0]['value'],
            'humedad': datos_clima['current_condition'][0]['humidity'],
            'viento': datos_clima['current_condition'][0]['windspeedKmph']
        }
    else:
        clima = None

    return render(request, 'core/periodistas/crudapi/index.html', {'clima': clima})

#API
#ViewSets para manejar las solicitudes http
class PeriodistaViewSet(viewsets.ModelViewSet):
    queryset = Periodista.objects.all().order_by('id')
    serializer_class = PeriodistaSerializer
    renderer_classes = [JSONRenderer]

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all().order_by('id')
    serializer_class = NoticiaSerializer
    renderer_classes = [JSONRenderer]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer
    renderer_classes = [JSONRenderer]
#ViewSets

# permisos
def user_in_group (user, group_name):
    return user.groups.filter(name=group_name).exists()

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if user_in_group(request.user, group_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request,"NO TIENES PERMISOS PARA ACCEDER A ESTA PAGINA")
                return redirect(to='index')
        return _wrapped_view
    return decorator

def register (request):
    aux = {
        'form' : UserCreationForm()
    }
    if request.method == 'POST':
        formulario = UserCreationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            grupos = Group.objects.get(name='periodista')
            usuario.groups.add(grupos)
            messages.success(request, "Usuario agregado correctamente")
            return redirect(to="periodistas")
        else:
            aux['form'] =  formulario

    return render(request, 'registration/register.html', aux)
# permisos


# Cosas generales
def index(request):
    noticias = Noticia.objects.all()
    categoria = Categoria.objects.all()
    noticia_aleatoria = choice(noticias)
    periodistas = Periodista.objects.all()

    aux = {
        'lista': categoria,
        'lista2': noticias,
        'lista3': periodistas,
        'noticia_aleatoria': noticia_aleatoria,
    }
    return render(request, 'core/index.html', aux)

def categoria (request):
    return render(request, 'core/categoria.html')

def contacto (request):
    return render(request, 'core/contacto.html')

def cuenta_lock (request):
    return render(request, 'core/cuenta_b.html')
# Cosas generales




#   periodistas

def periodistas(request):
    periodista_list = Periodista.objects.all()
    paginator = Paginator(periodista_list, 3)  # 3 periodistas por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'lista': page_obj,
    }
    return render(request, 'core/periodistas/index.html', context)  

@group_required('supervisor')
def periodistasadd (request):
    aux = {
        'form' : PeriodistaForm()
    }

    if request.method == 'POST' :
        formulario = PeriodistaForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Periodista creado correctamente')
        else:
            aux['form'] = formulario
            messages.error(request,'Error al crear el periodista')

    return render(request, 'core/periodistas/crud/add.html',aux)

@group_required('supervisor')
def periodistasupdate (request,id):
    periodista = Periodista.objects.get(id=id)
    aux = {
        'form' : PeriodistaForm(instance=periodista)
    }

    if request.method == 'POST' :
        formulario = PeriodistaForm(data=request.POST, instance=periodista, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request,'Periodista actualizado correctamente')
        else:
            aux['form'] = formulario
            messages.error(request,'Error al actualizar el empleado')

    return render(request, 'core/periodistas/crud/update.html', aux)

@group_required('supervisor')
@permission_required('core.delete_periodista')
def periodistasdelete (request,id):
    periodista = Periodista.objects.get(id=id)
    periodista.delete()

    return redirect(to="periodistas")

def perfilPerio(request,id):
    periodista = Periodista.objects.get(id=id)
    noticia = Noticia.objects.all()

    aux = {
        'periodista' : periodista,
        'noticia': noticia
    }

    return render(request, 'core/perfilPerio.html', aux)
    
#    fin periodistas




#    NOTICIAS

def single (request,id):
    noticias = Noticia.objects.get(id=id)
    aux = {
        'noticia' : noticias
    }
    return render(request, 'core/single.html',aux)




def noticias(request):
    noticias_list = Noticia.objects.all()
    paginator = Paginator(noticias_list, 3)  # 3 noticias por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'lista': page_obj,
    }
    return render(request, 'core/Noticias/noticias.html', context)


@group_required('periodista')
def noticiasadd (request):
    aux = {
        'form' : NoticiasForm()
    }
    
    if request.method == 'POST' :
        formulario = NoticiasForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Noticia agregada correctamente')
        else:
            aux['form'] = formulario
            messages.error(request,'Error al agregada la Noticia')

    return render(request, 'core/Noticias/Crud/addN.html', aux)


@group_required('supervisor')
def noticiasupdate (request,id):
    noticias = Noticia.objects.get(id=id)
    aux = {
        'form' : NoticiasForm(instance=noticias)
    }
    
    if request.method == 'POST' :
        formulario = NoticiasForm(data=request.POST, instance=noticias, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request,'Noticia modificada correctamente')
        else:
            aux['form'] = formulario
            messages.error(request,'Error al modificar la Noticia')

    return render(request, 'core/Noticias/Crud/updateN.html',aux)


@group_required('supervisor')
def noticiasdelete (request,id):
    noticias = Noticia.objects.get(id=id)
    noticias.delete()
    
    return redirect(to="noticias")

#    FIN NOTICIAS

#servicios
def servicios (request):
    return render(request, 'core/servicios.html')

def voucher (request):
    return render(request, 'core/voucher.html')