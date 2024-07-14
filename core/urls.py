from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('periodistas',PeriodistaViewSet)
router.register('noticias',NoticiaViewSet)
router.register('categorias',CategoriaViewSet)



urlpatterns = [
    path('',index, name="index"),
    path('categoria/', categoria, name="categoria"),
    path('contacto/', contacto, name="contacto"),
    path('register/', register, name="register"),
    path('cuenta_lock/', cuenta_lock, name="cuenta_lock"),

    path('periodistas/', periodistas, name="periodistas"),
    path('periodistas/add/', periodistasadd, name="periodistasadd"),
    path('periodistas/update/<id>/', periodistasupdate, name="periodistasupdate"),
    path('periodistas/delete/<id>/', periodistasdelete, name="periodistasdelete"),
    path('perfilPerio/<id>/', perfilPerio, name="perfilPerio"),
    
    path('single/<id>/', single, name="single"),
    path('noticias/', noticias, name="noticias"),
    path('noticias/add/', noticiasadd, name="noticiasadd"),
    path('noticias/update/<id>/', noticiasupdate, name="noticiasupdate"),
    path('noticias/delete/<id>/', noticiasdelete, name="noticiasdelete"),
    path('servicios/', servicios, name="servicios"),

    #api
    path('api/', include(router.urls)),
    path('noticiasapi/', noticiasapi, name="noticiasapi"),
    path('noticiadetalle/<id>/', noticiadetalle, name="noticiadetalle"),
    path('climaapi/', climaapi, name="climaapi"),

    #Baucher
    path('voucher/', voucher, name="voucher"),
<<<<<<< HEAD

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
=======
>>>>>>> 974e573ee1894c7ddfb3789a33240ed611937ca6
]