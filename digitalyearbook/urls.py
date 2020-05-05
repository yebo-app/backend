"""digitalyearbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from yearbook import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewset)
router.register(r'group', views.GroupViewSet)
router.register(r'yearbookuser', views.YearbookUserViewset)
router.register(r'institution', views.InstitutionViewset)
router.register(r'institutionyear', views.InstitutionYearViewset)
router.register(r'institutionyearprofile', views.InstitutionYearProfileViewset)
router.register(r'signature', views.SignatureViewSet)

urlpatterns = [
    path('yearbook/', include('yearbook.urls')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace= 'rest_framework')),
]
