from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class YearbookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=140, default= "")
   
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

class Institution(models.Model):
    institution_name = models.CharField(max_length=100, default= "")
    institution_city = models.CharField(max_length=100, default= "")
    institution_state = models.CharField(max_length=2, default= "")

    @classmethod
    def check_duplicate(cls, institution_name, institution_city, institution_state):
        for institution in Institution.objects.all():
            if institution.institution_name == institution_name and institution.institution_state == institution_state and institution.institution_city == institution_city:
                raise Exception("Institution with name: " + str(institution_name) + " in: " + str(institution_city) + ", " + str(institution_state) + " already exists.")

    @classmethod
    def create(cls, institution_name, institution_city="", institution_state=""):
        Institution.check_duplicate(institution_name, institution_city, institution_state)
        return cls(institution_name=institution_name, institution_city=institution_city, institution_state=institution_state)
  
    def set_institution_name(self, institution_name):
        Institution.check_duplicate(institution_name, self.institution_city, self.institution_state)
        self.institution_name=institution_name

    def set_institution_city(self, institution_city):
        Institution.check_duplicate(self.institution_name, institution_city, self.institution_state)
        self.institution_city = institution_city

    def set_institution_state(self, institution_state):
        Institution.check_duplicate(self.institution_name, self.set_institution_name, institution_state)
        self.institution_state = institution_state

    def set_institution_location(self, institution_city, institution_state):
        self.set_institution_city(institution_city)
        self.set_institution_state(institution_state)

    def __str__(self):
        return str(self.institution_name) + " | " + str(self.institution_city) + ", " + str(self.institution_state)

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

class InstitutionYearProfile(models.Model):
    yearbook_user = models.ForeignKey(YearbookUser, on_delete=models.CASCADE)
    institution_year = models.ForeignKey(InstitutionYear, on_delete=models.CASCADE)
    is_educator = models.BooleanField(default= False)
   
    @classmethod
    def check_duplicate(cls, yearbook_user, institution_year):
        for institution_year_profile in InstitutionYearProfile.objects.all():
            if institution_year_profile.yearbook_user == yearbook_user and institution_year_profile.institution_year == institution_year:
                raise Exception("InstitutionYearProfile with YearbookUser: " + str(yearbook_user) + " and InstitutionYear: " + str(institution_year) + " already exists.")

    @classmethod
    def create(cls, yearbook_user, institution_year, is_educator=False):
        InstitutionYearProfile.check_duplicate(yearbook_user, institution_year) 
        return cls(yearbook_user=yearbook_user, institution_year=institution_year, is_educator=is_educator)

    def set_is_educator(self, is_educator):
        self.is_educator = is_educator

    def __str__(self):
        return self.yearbook_user.user.first_name + " " + self.yearbook_user.user.last_name + " | " + str(self.institution_year) + (" | Educator" if self.is_educator else "")

class Signature(models.Model):
    author = models.ForeignKey(YearbookUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(InstitutionYearProfile, on_delete=models.CASCADE)
    signature = models.TextField(default= "")

    @classmethod
    def create(cls, author, recipient, signature=""):
        return cls(author=author, recipient=recipient, signature=signature)

    def set_signature(self, signature):
        self.signature = signature

    def __str__(self):
        return "Author: " + self.author.user.first_name + " | Recipient: " + self.recipient.yearbook_user.user.first_name + " | " + self.signature
