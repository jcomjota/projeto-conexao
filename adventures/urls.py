from django.urls import path
from . import views

app_name = 'adventures'

urlpatterns = [
    path('', views.AdventureListView.as_view(), name='list'),
    path('<slug:slug>/', views.AdventureDetailView.as_view(), name='detail'),
    path('categoria/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('admin/adventures/adventure/upload-image/', views.upload_adventure_image, name='upload_adventure_image'),
    path('admin/adventures/adventure/<int:adventure_id>/upload-image/', views.upload_adventure_image, name='upload_adventure_image_with_id'),
]