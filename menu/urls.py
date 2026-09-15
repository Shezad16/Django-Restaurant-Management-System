from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('item/<int:pk>/', views.menu_detail, name='menu_detail'),
]
