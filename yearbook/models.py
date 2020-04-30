from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class YearbookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=140)
    
    @classmethod
    def create(cls, user, bio):
        for yearbook_user in YearbookUser.objects.all():
            if yearbook_user.user == user:
                raise Exception("YearbookUser with User: " + str(user) + " already exists.")
        return cls(user=user, bio=bio)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def get_user_bio(self):
        return str(self.bio)

class Institution(models.Model):
    institution_name = models.CharField(max_length=100)

    @classmethod
    def create(cls, institution_name):
        for institution in Institution.objects.all():
            if institution.institution_name == institution_name:
                raise Exception("Institution with name: " + str(institution_name) + " already exists.")
        return cls(institution_name=institution_name)

    def __str__(self):
        return self.institution_name

class InstitutionYear(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    year = models.IntegerField()
    school_year = models.CharField(max_length=9)

    @classmethod
    def create(cls, institution, year):
        for institution_year in InstitutionYear.objects.all():
            if institution_year.institution == institution and institution_year.year == year:
                raise Exception("InstitutionYear with Institution: " + str(institution) + " and Year: " + str(year) + " already exists.")
        return cls(institution=institution, year=int(year), school_year=str(int(year - 1)) + "-" + str(year))

    def __str__(self):
        return str(self.institution) + " | " + str(self.school_year)

class InstitutionYearProfile(models.Model):
    yearbook_user = models.ForeignKey(YearbookUser, on_delete=models.CASCADE)
    institution_year = models.ForeignKey(InstitutionYear, on_delete=models.CASCADE)
    is_educator = models.BooleanField()
    
    @classmethod
    def create(cls, yearbook_user, institution_year, is_educator):
        for institution_year_profile in InstitutionYearProfile.objects.all():
            if institution_year_profile.yearbook_user == yearbook_user and institution_year_profile.institution_year == institution_year:
                raise Exception("InstitutionYearProfile with YearbookUser: " + str(yearbook_user) + " and InstitutionYear: " + str(institution_year) + " already exists.")
        return cls(yearbook_user=yearbook_user, institution_year=institution_year, is_educator=is_educator)

    def __str__(self):
        return self.yearbook_user.user.first_name + " " + self.yearbook_user.user.last_name + " | " + str(self.institution_year) + (" | Educator" if self.is_educator else "")
