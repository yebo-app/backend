from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import *
from yearbook.serializers import *
# from yearbook.models import *

from django.http import HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse("Hello from yearbook home")
    return render(request, 'yearbook/home.html')

def yearbookuser(request, id):
    context = {'user' : models.YearbookUser.objects.all().get(id=id)}
    return render(request, 'yearbook/user.html', context)

def yearbookusers(request):
    context = {'users' : list(models.YearbookUser.objects.all())}
    return render(request, 'yearbook/users.html', context)

def institution(request, id):
    institution = models.Institution.objects.all().get(id=id)
    institutionyears = institution.institutionyear_set.all().order_by('-year')
    context = {'institution' : institution, 'institutionyears' : institutionyears}
    return render(request, 'yearbook/institution.html', context)

def institutions(request):
    context = {'institutions' : list(models.Institution.objects.all())}
    return render(request, 'yearbook/institutions.html', context)

def institutionyear(request, id):
    institutionyear = models.InstitutionYear.objects.all().get(id=id)
    institutionyearprofiles = list(institutionyear.institutionyearprofile_set.all())
    context = {'institutionyear' : institutionyear, 'institutionyearprofiles' : institutionyearprofiles}
    return render(request, 'yearbook/institutionyear.html', context)

def institutionyearprofile(request, id):
    institutionyearprofile = models.InstitutionYearProfile.objects.all().get(id=id)
    signatures = list(models.Signature.objects.all().filter(recipient=institutionyearprofile))
    context = {'institutionyearprofile' : institutionyearprofile, 'signatures' : signatures}
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
