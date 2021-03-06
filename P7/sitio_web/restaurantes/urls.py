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
  url(r'buscar_ajax/', views.buscar_ajax, name='buscar_ajax'),
  #url(r'^buscar/', views.buscar, name='buscar'),
  #url(r'^buscar/<int:pag>', views.buscar, name='buscar'),
  #url(r'^modificar/<id>', views.modificar, name='modificar'),
  #path('borrar/<id>', views.borrar, name='borrar'),
  url(r'getDatos',views.getDatos,name='getDatos'),
  url(r'^form_buscar',views.buscar,name='form_buscar')
]
