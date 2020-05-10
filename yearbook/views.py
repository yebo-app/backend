from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import *
from yearbook.serializers import *
# from yearbook.models import *

from django.http import HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse("Hello from yearbook home")
    page_title = 'Home'
    context = {'page_title' : page_title}
    return render(request, 'yearbook/home.html', context)

def yearbookuser(request, id):
    user = models.YearbookUser.objects.all().get(id=id)
    page_title = user.user.first_name + " " + user.user.last_name
    context = {'user' : user, 'page_title' : page_title}
    return render(request, 'yearbook/user.html', context)

def yearbookusers(request):
    users = list(models.YearbookUser.objects.all())
    page_title = 'Users'
    context = {'users' : users, 'page_title' : page_title}
    return render(request, 'yearbook/users.html', context)

def institution(request, id):
    institution = models.Institution.objects.all().get(id=id)
    institutionyears = institution.institutionyear_set.all().order_by('-year')
    page_title = institution.institution_name
    context = {'institution' : institution, 'institutionyears' : institutionyears, 'page_title' : page_title}
    return render(request, 'yearbook/institution.html', context)

def institutions(request):
    institutions = list(models.Institution.objects.all())
    page_title = 'Institutions'
    context = {'institutions' : institutions, 'page_title' : page_title}
    return render(request, 'yearbook/institutions.html', context)

def institutionyear(request, id):
    institutionyear = models.InstitutionYear.objects.all().get(id=id)
    institutionyearprofiles = list(institutionyear.institutionyearprofile_set.all())
    page_title = institutionyear.school_year + " " + institutionyear.institution.institution_name
    context = {'institutionyear' : institutionyear, 'institutionyearprofiles' : institutionyearprofiles, 'page_title' : page_title}
    return render(request, 'yearbook/institutionyear.html', context)

def institutionyearprofile(request, id):
    institutionyearprofile = models.InstitutionYearProfile.objects.all().get(id=id)
    signatures = list(models.Signature.objects.all().filter(recipient=institutionyearprofile))
    page_title = str(institutionyearprofile.yearbook_user) + " " + institutionyearprofile.institution_year.school_year + " " + institutionyearprofile.institution_year.institution.institution_name
    context = {'institutionyearprofile' : institutionyearprofile, 'signatures' : signatures, 'page_title' : page_title}
    return render(request, 'yearbook/institutionyearprofile.html', context)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class YearbookUserViewset(viewsets.ModelViewSet):
    queryset = models.YearbookUser.objects.all()
    serializer_class = YearbookUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class InstitutionViewset(viewsets.ModelViewSet):
    queryset = models.Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

class InstitutionYearViewset(viewsets.ModelViewSet):
    queryset = models.InstitutionYear.objects.all()
    serializer_class = InstitutionYearSerializer
    permission_classes = [permissions.IsAuthenticated]

class InstitutionYearProfileViewset(viewsets.ModelViewSet):
    queryset = models.InstitutionYearProfile.objects.all()
    serializer_class = InstitutionYearProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class SignatureViewSet(viewsets.ModelViewSet):
    queryset = models.Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [permissions.IsAuthenticated]
