from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from adminscopus import views


urlpatterns = [
    url('^build/consultas/(?P<country>.+)/$', views.consultas.as_view()),
    path('build/proyecto', views.proyecto.as_view()),
    url('^extraccion/(?P<country>.+)/$', views.extraccion.as_view()),
    url('^procesamiento/(?P<country>.+)/$', views.procesamiento.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
