from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.MaterialListView, name='list'),
    path('categoria/<slug:slug>/', views.MaterialCategoryView, name='category'),
    path('download/<int:pk>/', views.MaterialDownloadView, name='download'),
] 