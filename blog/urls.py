from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.category_list, name='category_list'),
    path('write/new/', views.post_create, name='post_create'),
    path('write/edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('write/delete/<slug:slug>/', views.post_delete, name='post_delete'),
    path('settings/', views.site_settings, name='site_settings'),
    path('upload-image/', views.upload_image, name='upload_image'),
]
