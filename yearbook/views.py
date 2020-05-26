from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from django.contrib.auth.models import *
from django.contrib.auth import update_session_auth_hash
from yearbook.serializers import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from yearbook.forms import *
from yearbook.models import *
from django.forms import modelformset_factory, formset_factory
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.mail import send_mail
import digitalyearbook

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
    for iyp in InstitutionYearProfile.objects.all().filter(yearbook_user=yearbook_user).order_by('institution_year__year'):
        institution = iyp.institution_year.institution
        if institution not in history.keys():
            history[institution] = []
        history[institution].append(iyp)
    
    # Register IYP Form
    instance = get_object_or_404(YearbookUser, id=id)
    register_form = InstitutionYearProfileCreationForm(request.POST or None)
    if register_form.is_valid():
        institution = register_form.cleaned_data.get("institution")
        start_year = register_form.cleaned_data.get("start_year")
        end_year = register_form.cleaned_data.get("end_year")
        instance.register(institution, start_year, end_year)
        messages.success(request, 'Profiles created successfully.')
        return redirect(request.user.yearbookuser.get_absolute_url())
    
    # Invite Friend Form
    invite_friend_form = InviteFriendForm(request.POST or None)
    if invite_friend_form.is_valid():
        subject = f'{request.user.first_name} is inviting you to join yebo!'
        message = f'{request.user.first_name} is inviting you to join yebo!\n\nyebo is a digital yearbook platform that allows you to connect with your friends from school. You can create profiles for each year you were in school, view your friends\' profiles, and even write them a signature!\n\nJoin yebo today for free!\nhttp://127.0.0.1:8000/register/\nView {request.user.first_name}\'s profile here: { request.build_absolute_uri() }'
        from_email = digitalyearbook.settings.EMAIL_HOST_USER
        to_email = [invite_friend_form.cleaned_data['friend_email']]
        fail_silently = False

        send_mail(
            subject,
            message,
            from_email,
            to_email,
            fail_silently
        )
        messages.success(request, "Invite sent successfully.")
        return redirect(request.user.yearbookuser.get_absolute_url())

    context = {'yearbook_user' : yearbook_user, 'page_title' : page_title, 'history' : history, 'register_form' : register_form, 'invite_friend_form' : invite_friend_form}
    return render(request, 'yearbook/user.html', context)

def yearbookusers(request):
    users = list(YearbookUser.objects.all())
    page_title = 'Users'
    context = {'users' : users, 'page_title' : page_title}
    return render(request, 'yearbook/users.html', context)

def settings(request, id):
    page_title = 'Settings'

    yearbook_user = get_object_or_404(YearbookUser, id=id)
    user = yearbook_user.user

    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=user) # Django User ModelForm
        yearbookuser_update_form = YearbookUserUpdateForm(request.POST, request.FILES, instance=yearbook_user) # YearbookUser Model Form
        if yearbookuser_update_form.is_valid() and user_update_form.is_valid():
            user_update_form.save()
            yearbookuser_update_form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('/settings/' + str(request.user.yearbookuser.id))
    else:
        user_update_form = UserUpdateForm(instance=user)
        yearbookuser_update_form = YearbookUserUpdateForm(instance=yearbook_user)

    # User Delete Form
    user_delete_form = IYPDeleteForm(request.POST or None, instance=user)
    if user_delete_form.is_valid() and "delete" in request.POST:
        user_delete_form.instance.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('home')

    password_change_form = PasswordChangeForm(data=request.POST or None, user=user)
    if password_change_form.is_valid() and "change" in request.POST:
        password_change_form.save()
        messages.success(request, 'Password changed successfully. Please login again.')
        return redirect('home')
    if password_change_form.errors:
        messages.error(request, 'Unable to change password. Please try again.')

    context = {'yearbook_user' : yearbook_user, 'page_title' : page_title, 'user_update_form' : user_update_form, 'yearbookuser_update_form' : yearbookuser_update_form, 'user_delete_form' : user_delete_form, 'password_change_form' : password_change_form}
    return render(request, 'yearbook/accountsettings.html', context)

def institution(request, id):
    institution = Institution.objects.all().get(id=id)
    page_title = institution.institution_name
    
    institution_join_form = InstitutionJoinForm(request.POST or None)
    if institution_join_form.is_valid():
        institutionyears = institution_join_form.cleaned_data.get("institutionyears")
        print(institutionyears)
        request.user.yearbookuser.register_years(institutionyears)
        return redirect(request.user.yearbookuser.get_absolute_url())

    url_parameter = request.GET.get("q")
    if url_parameter:
        institutionyears = list(institution.institutionyear_set.filter(school_year__icontains=url_parameter))
    else:
        institutionyears = institution.institutionyear_set.all().order_by('-year')
    if request.is_ajax():
        html = render_to_string(
            template_name="yearbook/institution-partial.html",
            context= {"institutionyears" : institutionyears}
        )
        data_dict = {"html_from_view" : html}
        return JsonResponse(data=data_dict, safe=False)

    context = {'institution' : institution, 'institutionyears' : institutionyears, 'page_title' : page_title, 'institution_join_form' : institution_join_form}
    return render(request, 'yearbook/institution.html', context)

def institutions(request):
    #Institution Creation Form
    page_title = 'Institutions'
    if request.method == 'POST':
        form = InstitutionCreationForm(request.POST)
        if form.is_valid():
            created = form.save(commit= False)
            Institution.create(created.institution_name, created.institution_city, created.institution_state, created.institution_year_founded)
            messages.success(request, 'Institution created successfully.')
            return redirect('/institutions')
    else:
        form = InstitutionCreationForm()
        #AJAX Search
        url_parameter = request.GET.get("q")
        if url_parameter:
            institutions = list(Institution.objects.filter(institution_name__icontains=url_parameter))
        else:
            institutions = list(Institution.objects.all())
        #AJAX Response
        if request.is_ajax():
            html = render_to_string(
                template_name="yearbook/institutions-partial.html",
                context={"institutions": institutions}
            )
            data_dict = {"html_from_view" : html}
            return JsonResponse(data=data_dict, safe=False)
    
    context = {'institutions' : institutions, 'page_title' : page_title, 'form' : form}
    return render(request, 'yearbook/institutions.html', context)

def institutionyear(request, id):
    institutionyear = InstitutionYear.objects.all().get(id=id)
    page_title = institutionyear.school_year + " " + institutionyear.institution.institution_name

    url_parameter = request.GET.get("q")
    if url_parameter:
        iyp1 = list(institutionyear.institutionyearprofile_set.filter(yearbook_user__user__first_name__icontains=url_parameter))
        iyp2 = list(institutionyear.institutionyearprofile_set.filter(yearbook_user__user__last_name__icontains=url_parameter))
        institutionyearprofiles = set(iyp1+iyp2)
    else:
        institutionyearprofiles = list(institutionyear.institutionyearprofile_set.all())
    if request.is_ajax():
        html = render_to_string(
            template_name="yearbook/institutionyear-partial.html",
            context = {"institutionyearprofiles" : institutionyearprofiles}
        )
        data_dict = {"html_from_view" : html}
        return JsonResponse(data=data_dict, safe=False)    

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

    signatureupdateforms = []
    signaturedeleteforms = []
    # If there are forms that the user can update
    if queryset:
        # Loop through all signatures to create respective update forms
        for signature in queryset:
            instance = signature
            update_form = SignatureUpdateForm(request.POST or None, instance=instance)
            delete_form = SignatureDeleteForm(request.POST or None, instance=instance)
            signatureupdateforms.append((update_form, instance, instance.id))
            signaturedeleteforms.append((delete_form, instance, instance.id))
            if request.method == "POST":
                for signatureupdateformtuple in signatureupdateforms:
                    if "update" + str(signatureupdateformtuple[2]) in request.POST:
                        # Select this form and save changes
                        u_form = signatureupdateformtuple[0]
                        if u_form.is_valid():
                            u_form.save()
                            messages.success(request, 'Signature updated successfully.')
                            return redirect(institutionyearprofile.get_absolute_url())
                for signaturedeleteformtuple in signaturedeleteforms:
                    if "delete" + str(signaturedeleteformtuple[2]) in request.POST:
                        d_form = signaturedeleteformtuple[0]
                        if d_form.is_valid():
                            d_form.instance.delete()
                            messages.success(request, 'Signature deleted successfully.')
                            return redirect(institutionyearprofile.get_absolute_url())

    # IYP Update Form
    instance = get_object_or_404(InstitutionYearProfile, id=id)
    iypupdateform = IYPUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if iypupdateform.is_valid():
        iypupdateform.save()
        messages.success(request, 'Profile updated successfully.')
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

    # IYP Delete Form
    iypdeleteform = IYPDeleteForm(request.POST or None, instance=instance)
    if iypdeleteform.is_valid():
        iypdeleteform.instance.delete()
        return redirect(request.user.yearbookuser.get_absolute_url())
    
    context = {'institutionyearprofile' : institutionyearprofile, 'signatures' : signatures, 'page_title' : page_title, 'iypupdateform' : iypupdateform, 'signatureform' : signatureform, 'signatureupdateforms' : signatureupdateforms if queryset is not None else [], 'signaturedeleteforms' : signaturedeleteforms if queryset is not None else [], 'iypdeleteform' : iypdeleteform}
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
            # messages.success(request, f'Account created for {username}')
            messages.success(request, 'Account created successfully.')
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
