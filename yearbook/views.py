from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from django.contrib.auth.models import *
from yearbook.serializers import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from yearbook.forms import *
from yearbook.models import *

from django.http import HttpResponse

# Create your views here.

def home(request):
    # return HttpResponse("Hello from yearbook home")
    page_title = 'Home'
    context = {'page_title' : page_title}
    return render(request, 'yearbook/home.html', context)

def yearbookuser(request, id):
    user = YearbookUser.objects.all().get(id=id)
    page_title = user.user.first_name + " " + user.user.last_name
    context = {'user' : user, 'page_title' : page_title}
    return render(request, 'yearbook/user.html', context)

def yearbookusers(request):
    users = list(YearbookUser.objects.all())
    page_title = 'Users'
    context = {'users' : users, 'page_title' : page_title}
    return render(request, 'yearbook/users.html', context)

def institution(request, id):
    institution = Institution.objects.all().get(id=id)
    institutionyears = institution.institutionyear_set.all().order_by('-year')
    page_title = institution.institution_name
    context = {'institution' : institution, 'institutionyears' : institutionyears, 'page_title' : page_title}
    return render(request, 'yearbook/institution.html', context)

def institutions(request):
    institutions = list(Institution.objects.all())
    page_title = 'Institutions'
    context = {'institutions' : institutions, 'page_title' : page_title}
    return render(request, 'yearbook/institutions.html', context)

def institutionyear(request, id):
    institutionyear = InstitutionYear.objects.all().get(id=id)
    institutionyearprofiles = list(institutionyear.institutionyearprofile_set.all())
    page_title = institutionyear.school_year + " " + institutionyear.institution.institution_name
    context = {'institutionyear' : institutionyear, 'institutionyearprofiles' : institutionyearprofiles, 'page_title' : page_title}
    return render(request, 'yearbook/institutionyear.html', context)

def institutionyearprofile(request, id):
    institutionyearprofile = InstitutionYearProfile.objects.all().get(id=id)
    signatures = list(Signature.objects.all().filter(recipient=institutionyearprofile))
    page_title = str(institutionyearprofile.yearbook_user) + " " + institutionyearprofile.institution_year.school_year + " " + institutionyearprofile.institution_year.institution.institution_name
    context = {'institutionyearprofile' : institutionyearprofile, 'signatures' : signatures, 'page_title' : page_title}
    return render(request, 'yearbook/institutionyearprofile.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        yearbook_user_form = YearbookUserRegistrationForm(request.POST)

        if user_form.is_valid() and yearbook_user_form.is_valid():
            user = user_form.save()
            yearbook_user = yearbook_user_form.save(commit=False) # Don't save immediately to DB

            yearbook_user.user = user # Pass in User from user form into YU form
            yearbook_user.save() # Now save YU object with User object (one-to-one field)

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            messages.success(request, f'Account created for {username}')
            return redirect('yu-update')
    else:
        user_form = UserRegistrationForm()
        yearbook_user_form = YearbookUserRegistrationForm()

    context = {'user_form' : user_form, 'yearbook_user_form' : yearbook_user_form}
    return render(request, 'yearbook/register.html', context)

def sign(request, id):
    if request.method == 'POST':
        form = SignatureForm(request.POST)
        if form.is_valid():
            signed = form.save(commit= False)
            signed.author = request.YearbookUser
            signed.recipient = request.InstitutionYearProfile
            form.save()
            return redirect('institutionyearprofile.html')
    else:
        form = SignatureForm()
    return render(request, 'yearbook/institutionyearprofile.html', {'form': form})

def updateyearbookuser(request):
    if request.method == 'POST':
        form = YearbookUserUpdateForm(request.POST)
        if form.is_valid():
            updated = form.save(commit= False)
            updated.set_bio(updated)
            return redirect('home')
    else:
        form = YearbookUserUpdateForm()
    return render(request, 'yearbook/yearbookuserupdate.html', {'form': form})
'''
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
'''
