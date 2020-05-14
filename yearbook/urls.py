from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('yearbookuserupdate/', views.updateyearbookuser, name='yu-update'),
    path('login/', auth_views.LoginView.as_view(template_name='yearbook/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='yearbook/logout.html'), name='logout'),
    path('profile/<id>', views.institutionyearprofile, name='institutionyearprofile'),
    path('year/<id>', views.institutionyear, name='institutionyear'),
    path('institutions/<id>', views.institution, name='institution'),
    path('institutions', views.institutions, name='institutions'),
    path('u/<id>', views.yearbookuser, name='user'),
    path('u', views.yearbookusers, name='users'),
]
