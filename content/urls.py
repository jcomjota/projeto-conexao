from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.about, name='about'),
    path('como-funciona/', views.how_it_works, name='how_it_works'),
    path('regras-gerais/', views.general_rules, name='general_rules'),
    path('contato/', views.contact, name='contact'),
    path('termos/', views.terms, name='terms'),
    path('privacidade/', views.privacy, name='privacy'),
] 