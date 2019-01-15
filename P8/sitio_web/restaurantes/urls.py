from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^test_template/$', views.test_template, name='test_template'),
  url(r'^work', views.work, name='work'),
  #url(r'^login', views.login, name='login'),
  #url(r'^log_out', views.log_out, name='log_out'),
  #url(r'^sing_up', views.sign_up, name='sing_up'),
  #url(r'^update_info', views.update_info, name='update_info'),
  #url(r'^info', views.info, name='info'),   
  path('buscar/<int:pag>/', views.buscar, name='buscar'),
  url(r'^buscar/', views.buscar, name='buscar'),
  #url(r'^buscar/<int:pag>', views.buscar, name='buscar'),
  #url(r'^modificar/<id>', views.modificar, name='modificar'),
  #path('borrar/<id>', views.borrar, name='borrar'),
  path(r'mapa/(?P<nombre_res>\d+)', views.buscar_mapa, name='mapa'),
  url(r'^form_buscar',views.buscar,name='form_buscar'),
  url(r'^grafico/', views.grafico, name='grafico'),
  path(r'grafico_ajax/', views.grafico_ajax, name='grafico_ajax'),
  url(r'modDatos',views.modDatosGraf,name='modDatos'),
  path(r'not_found/',views.page_not_found,name='not_found')
]
