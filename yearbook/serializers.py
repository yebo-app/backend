from django.contrib.auth.models import *
from rest_framework import serializers
from yearbook import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class YearbookUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.YearbookUser
        fields = ['user', 'bio']
  
class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Institution
        fields = ['institution_name', 'institution_city', 'institution_state']
    

class InstitutionYearSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.InstitutionYear
        fields = ['institution','year', 'school_year']

class InstitutionYearProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.InstitutionYearProfile
        fields = ['yearbook_user', 'institution_year', 'is_educator']

class SignatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Signature
        fields = ['author', 'recipient', 'signature']

