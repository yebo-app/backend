from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('signatureupdate/<id>', views.signatureupdate, name='signatureupdate'),
    path('yearbookuserupdate/<id>', views.updateyearbookuser, name='yu-update'),
    path('createinstitution/', views.createinstitution, name= 'create-institution'),
    path('registeriyp/<id>', views.registeriyp, name = 'registeriyp'),
    path('iypupdate/<id>', views.iypupdate, name = 'iypupdate'),
    path('login/', auth_views.LoginView.as_view(template_name='yearbook/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='yearbook/logout.html'), name='logout'),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='yearbook/passwordresetform.html'), name='reset_password'),
    path('passwordresetsent/', auth_views.PasswordResetDoneView.as_view(template_name='yearbook/passwordresetsent.html'), name='password_reset_done'),
    path('passwordreset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='yearbook/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('passwordresetcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name='yearbook/passwordresetcomplete.html'), name='password_reset_complete'),
    path('profile/<id>', views.institutionyearprofile, name='institutionyearprofile'),
    path('year/<id>', views.institutionyear, name='institutionyear'),
    path('institutions/<id>', views.institution, name='institution'),
    path('institutions', views.institutions, name='institutions'),
    path('u/<id>', views.yearbookuser, name='user'),
    path('u', views.yearbookusers, name='users'),
]
