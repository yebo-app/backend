from django.db import models
from django.contrib.auth.models import User
from notifications.base.models import AbstractNotification
from datetime import date

# Create your models here.

class YearbookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='default_profile_picture.png')
    bio = models.CharField(max_length=140, default="")
    
    def register_year(self, institutionyear):
        iyp = InstitutionYearProfile.create(self, institutionyear)
        iyp.save()

    def register_years(self, institutionyears):
        for institutionyear in institutionyears:
            iyp = InstitutionYearProfile.create(self, institutionyear)
            iyp.save()

    def register(self, institution, start_year, end_year):
        if start_year > end_year:
            raise Exception("Start Year: " + str(start_year) + " cannot be greater than End Year: " + str(end_year))
        if start_year < institution.institution_year_founded:
            raise Exception ("Start Year: " + str(start_year) + " cannot be less than Founding Year of the Institution: " + str(institution.institution_year_founded))
        for year in range(start_year + 1, end_year + 1):
            try:
                iy = InstitutionYear.objects.all().get(institution=institution, year=year)
            except InstitutionYear.DoesNotExist:
                iy = InstitutionYear.create(institution, year)
                iy.save()
            iyp = InstitutionYearProfile.create(self, iy)
            iyp.save()
        institution.update_unique_users()
    
    def write_signature(self, recipient, message):
        s = Signature.create(self, recipient, message)
        s.save()
        return s
    
    def set_bio(self, bio):
        self.bio = bio

    @classmethod
    def check_duplicate(cls, user):
         for yearbook_user in YearbookUser.objects.all():
            if yearbook_user.user == user:
                raise Exception("YearbookUser with User: " + str(user) + " already exists.")

    @classmethod
    def create(cls, user, bio=""):
        YearbookUser.check_duplicate(user)
        return cls(user=user, bio=bio)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def get_absolute_url(self):
        return "/u/%i" % self.id

class Institution(models.Model):
    institution_name = models.CharField(max_length=100, default= "")
    institution_city = models.CharField(max_length=100, default= "")
    institution_state = models.CharField(max_length=2, default= "")
    institution_year_founded = models.IntegerField(default=date.today().year)
    logo = models.ImageField(upload_to='logos', default='default_institution_logo.png')
    unique_members = models.IntegerField(default=0)

    @classmethod
    def check_duplicate(cls, institution_name, institution_city, institution_state):
        for institution in Institution.objects.all():
            if institution.institution_name == institution_name and institution.institution_state == institution_state and institution.institution_city == institution_city:
                raise Exception("Institution with name: " + str(institution_name) + " in: " + str(institution_city) + ", " + str(institution_state) + " already exists.")

    @classmethod
    def create(cls, institution_name, institution_city, institution_state, institution_year_founded):
        Institution.check_duplicate(institution_name, institution_city, institution_state)
        institution = cls(institution_name=institution_name, institution_city=institution_city, institution_state=institution_state, institution_year_founded=institution_year_founded)
        institution.save()
        for year in range(institution_year_founded, date.today().year + 1):
            iy = InstitutionYear.create(institution, year)
            iy.save()
        return institution
  
    def set_institution_name(self, institution_name):
        #Institution.check_duplicate(institution_name, self.institution_city, self.institution_state)
        self.institution_name=institution_name

    def set_institution_city(self, institution_city):
        #Institution.check_duplicate(self.institution_name, institution_city, self.institution_state)
        self.institution_city = institution_city

    def set_institution_state(self, institution_state):
        #Institution.check_duplicate(self.institution_name, self.set_institution_name, institution_state)
        self.institution_state = institution_state

    def update_unique_users(self):
        yu_set = []
        for iy in list(self.institutionyear_set.all()):
            for iyp in list(iy.institutionyearprofile_set.all()):
                yu_set.append(iyp.yearbook_user)
        self.unique_members = len(set(yu_set))
        self.save()
        return self.unique_members

    def __str__(self):
        return str(self.institution_name) + " | " + str(self.institution_city) + ", " + str(self.institution_state)

    def get_absolute_url(self):
        return "/institutions/%i" % self.id

class InstitutionYear(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    year = models.IntegerField(default= 0)
    school_year = models.CharField(max_length=9, default= "")

    @classmethod
    def check_duplicate(cls, institution, year):
        for institution_year in InstitutionYear.objects.all():
            if institution_year.institution == institution and institution_year.year == year:
                raise Exception("InstitutionYear with Institution: " + str(institution) + " and Year: " + str(year) + " already exists.")

    @classmethod
    def create(cls, institution, year):
        InstitutionYear.check_duplicate(institution, year)
        return cls(institution=institution, year=int(year), school_year=str(int(year - 1)) + "-" + str(year))

    def set_institution_year(self, year):
        InstitutionYear.check_duplicate(self.institution, year)
        self.year = year
        self.school_year= str(int(year - 1)) + "-" + str(year)

    def __str__(self):
        return str(self.institution) + " | " + str(self.school_year)

    def get_absolute_url(self):
        return "/year/%i" % self.id

class InstitutionYearProfile(models.Model):
    yearbook_user = models.ForeignKey(YearbookUser, on_delete=models.CASCADE)
    yearbook_picture = models.ImageField(upload_to='yearbook_pictures', default='default_profile_picture.png')
    yearbook_quote = models.CharField(max_length=140, default="")
    institution_year = models.ForeignKey(InstitutionYear, on_delete=models.CASCADE)
   
    @classmethod
    def check_duplicate(cls, yearbook_user, institution_year):
        for institution_year_profile in InstitutionYearProfile.objects.all():
            if institution_year_profile.yearbook_user == yearbook_user and institution_year_profile.institution_year == institution_year:
                raise Exception("InstitutionYearProfile with YearbookUser: " + str(yearbook_user) + " and InstitutionYear: " + str(institution_year) + " already exists.")

    @classmethod
    def create(cls, yearbook_user, institution_year, yearbook_quote=""):
        InstitutionYearProfile.check_duplicate(yearbook_user, institution_year) 
        return cls(yearbook_user=yearbook_user, institution_year=institution_year, yearbook_quote=yearbook_quote)

    def set_yearbook_quote(self, yearbook_quote):
        self.yearbook_quote = yearbook_quote

    def __str__(self):
        return self.yearbook_user.user.first_name + " " + self.yearbook_user.user.last_name + " | " + str(self.institution_year)

    def get_absolute_url(self):
        return "/profile/%i" % self.id

class Signature(models.Model):
    author = models.ForeignKey(YearbookUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(InstitutionYearProfile, on_delete=models.CASCADE)
    signature = models.CharField(max_length= 280)

    @classmethod
    def create(cls, author, recipient, signature=""):
        return cls(author=author, recipient=recipient, signature=signature)

    def set_signature(self, signature):
        self.signature = signature

    def __str__(self):
        return "Author: " + self.author.user.first_name + " | Recipient: " + self.recipient.yearbook_user.user.first_name + " | " + self.signature