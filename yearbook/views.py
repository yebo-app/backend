from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from django.contrib.auth.models import *
from yearbook.serializers import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from yearbook.forms import *
from yearbook.models import *
from django.forms import modelformset_factory, formset_factory
from django.core.exceptions import ValidationError

from django.http import HttpResponse

# Create your views here.

def home(request):
    page_title = 'Home'
    context = {'page_title' : page_title}
    return render(request, 'yearbook/home.html', context)

def yearbookuser(request, id):
    yearbook_user = YearbookUser.objects.all().get(id=id)
    page_title = yearbook_user.user.first_name + " " + yearbook_user.user.last_name

    # Construct education history dictionary
    history = {}
    for iyp in InstitutionYearProfile.objects.all().filter(yearbook_user=yearbook_user):
        institution = iyp.institution_year.institution
        if institution not in history.keys():
            history[institution] = []
        history[institution].append(iyp)
    
    # Yearbook User Update Form
    instance = get_object_or_404(YearbookUser, id=id)
    update_form = YearbookUserUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if update_form.is_valid():
        update_form.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect(instance.get_absolute_url())

    # Register IYP Form
    instance = get_object_or_404(YearbookUser, id=id)
    register_form = InstitutionYearProfileCreationForm(request.POST or None)
    if register_form.is_valid() and not update_form.is_valid():
        institution = register_form.cleaned_data.get("institution")
        start_year = register_form.cleaned_data.get("start_year")
        end_year = register_form.cleaned_data.get("end_year")
        is_educator = register_form.cleaned_data.get("is_educator")
        instance.register(institution, start_year, end_year, is_educator)
        messages.success(request, 'Profiles Created')
        return redirect(request.user.yearbookuser.get_absolute_url())
    
    context = {'yearbook_user' : yearbook_user, 'page_title' : page_title, 'history' : history, 'update_form' : update_form, 'register_form' : register_form}    
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
    if request.method == 'POST':
        form = InstitutionCreationForm(request.POST)
        if form.is_valid():
            created = form.save(commit= False)
            Institution.create(created.institution_name, created.institution_city, created.institution_state, created.institution_year_founded)
            messages.success(request, 'Institution Created')
            return redirect('/institutions')
    else:
        form = InstitutionCreationForm()

    context = {'institutions' : institutions, 'page_title' : page_title, 'form' : form}
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

    if request.user.is_authenticated:
        queryset = Signature.objects.filter(author=request.user.yearbookuser)
    else:
        queryset = None

    
    signatureforms = []
    i = 0
    for signature in queryset:
        instance = get_object_or_404(Signature, id=signature.id)
        form = SignatureUpdateForm(request.POST or None, instance=instance)
        signatureforms.append((form, signature, i))
        if request.method == "POST":
            for j in range(i + 1):
                if "default" + str(j) in request.POST:
                    form = signatureforms[j][0]
                    if form.is_valid():
                        form.save()
                        return redirect(institutionyearprofile.get_absolute_url())
        i += 1

    # IYP Update Form
    instance = get_object_or_404(InstitutionYearProfile, id=id)
    iypupdateform = IYPUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if iypupdateform.is_valid():
        iypupdateform.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect(instance.get_absolute_url())

    # Signature Writing Form
    if request.method == "POST":
        signatureform = SignatureForm(request.POST)
        if signatureform.is_valid():# and not signatureupdateformset.is_valid(): # and True not in [form[0].is_valid() for form in signatureupdateforms]:
            signature = signatureform.save(commit=False)
            signature.author = request.user.yearbookuser
            signature.recipient = institutionyearprofile
            signature.save()
            return redirect(institutionyearprofile.get_absolute_url())
    else:
        signatureform = SignatureForm()
    
    context = {'institutionyearprofile' : institutionyearprofile, 'signatures' : signatures, 'page_title' : page_title, 'iypupdateform' : iypupdateform, 'signatureform' : signatureform, 'signatureforms' : signatureforms}

    return render(request, 'yearbook/institutionyearprofile.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        yearbook_user_form = YearbookUserRegistrationForm(request.POST)

        if user_form.is_valid() and yearbook_user_form.is_valid():
            user = user_form.save()
            email = user_form.cleaned_data['email']

            yearbook_user = yearbook_user_form.save(commit=False) # Don't save immediately to DB

            yearbook_user.user = user # Pass in User from user form into YU form
            yearbook_user.save() # Now save YU object with User object (one-to-one field)

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            messages.success(request, f'Account created for {username}')
            return redirect('/login/')
    else:
        user_form = UserRegistrationForm()
        yearbook_user_form = YearbookUserRegistrationForm()

    context = {'user_form' : user_form, 'yearbook_user_form' : yearbook_user_form}
    return render(request, 'yearbook/register.html', context)

# REMOVE THIS and yearbookuserupdate.html
def updateyearbookuser(request, id):
    instance = get_object_or_404(YearbookUser, id=id)
    form = YearbookUserUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect(instance.get_absolute_url())
    return render(request, 'yearbook/yearbookuserupdate.html', {'form' : form, 'yearbookuser' : instance})

# REMOVE THIS and iypupdate.html
def iypupdate(request, id):
    instance = get_object_or_404(InstitutionYearProfile, id=id)
    form = IYPUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect(instance.get_absolute_url())
    return render(request, 'yearbook/iypupdate.html', {'form' : form, 'institutionyearprofile' : instance})

# REMOVE THIS and signatureupdate.html
def signatureupdate(request, id):
    instance = get_object_or_404(Signature, id=id)
    form = SignatureUpdateForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Signature Updated Successfully')
        return redirect(instance.recipient.get_absolute_url())
    return render(request, 'yearbook/signatureupdate.html', {'form' : form, 'signature' : instance})

# REMOVE THIS and createinstitution.html
def createinstitution(request):
    if request.method == 'POST':
        form = InstitutionCreationForm(request.POST)
        if form.is_valid():
            created = form.save(commit= False)
            Institution.create(created.institution_name, created.institution_city, created.institution_state, created.institution_year_founded)
            messages.success(request, 'Institution Created')
            return redirect('/institutions/')
    else:
        form = InstitutionCreationForm()
    context = {'form' : form}
    return render(request, 'yearbook/createinstitution.html', {'form': form})

# REMOVE THIS and registeriyp.html
def registeriyp(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(YearbookUser, id=id)
        form = InstitutionYearProfileCreationForm(request.POST)
        if form.is_valid():
            institution = form.cleaned_data.get("institution")
            start_year = form.cleaned_data.get("start_year")
            end_year = form.cleaned_data.get("end_year")
            is_educator = form.cleaned_data.get("is_educator")
            instance.register(institution, start_year, end_year, is_educator)
            messages.success(request, 'Profiles Created')
            return redirect(request.user.yearbookuser.get_absolute_url())
    else:
        form = InstitutionYearProfileCreationForm()
    context = {'form': form}
    return render(request, 'yearbook/registeriyp.html', {'form': form})

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
