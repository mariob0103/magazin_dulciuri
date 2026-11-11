from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('produse', views.afis_produse, name='produse'),
    path('mesaje', views.afisare, name='mesaje'),
    path('log', views.log, name='log'),
    path('istoric', views.istoric, name='istoric'),
    path('despre', views.despre, name='despre'),
    path('contact', views.in_lucru, name='contact'),
    path('cos_virtual', views.in_lucru, name='cos_virtual'),
    re_path( r'^accesare(?P<id>\d+)/?$',views.detalii_accesare,name='detalii_accesare'),
]
