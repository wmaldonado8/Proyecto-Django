from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginPage, name='auth'),
    path('salir', views.logoutPage, name='logout'),
]
