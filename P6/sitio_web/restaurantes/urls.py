from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^test_template/$', views.test_template, name='test_template'),
  url(r'^work', views.work, name='work'),
  #url(r'^login', views.login, name='login'),
  #url(r'^log_out', views.log_out, name='log_out'),
  #url(r'^sing_up', views.sign_up, name='sing_up'),
  #url(r'^update_info', views.update_info, name='update_info'),
  #url(r'^info', views.info, name='info'),   
  path('buscar', views.buscar, name='buscar'),
  #url(r'^modificar/<id>', views.modificar, name='modificar'),
  #path('borrar/<id>', views.borrar, name='borrar'),
  url(r'^form_buscar',views.buscar,name='form_buscar'),
  path('buscar_plato',views.buscar_plato,name='buscar_plato'),
  path('borrar_plato',views.borrar_plato,name='borrar_plato'),
  url(r'^accounts', include('allauth.urls')),
  #url(r'sing_up', include('allauth.urls')),
  #url(r'login', views.login, name='log_in'),
  #url(r'log_out',views.log_out,name='log_out')
]
