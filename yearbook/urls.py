from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('institutions/year/profile/<id>', views.institutionyearprofile, name='institutionyearprofile'),
    path('institutions/year/<id>', views.institutionyear, name='institutionyear'),
    path('institutions/<id>', views.institution, name='institution'),
    path('institutions', views.institutions, name='institutions'),
    path('u/<id>', views.yearbookuser, name='user'),
    path('u', views.yearbookusers, name='users'),
]
