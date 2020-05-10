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
        fields = ['url', 'user', 'bio']

    def create(self, validated_data):
        instance = YearbookUserSerializer.Meta.model.create(**validated_data)
        instance.save()
        return instance
  
class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Institution
        fields = ['url', 'institution_name', 'institution_city', 'institution_state', 'institution_year_founded']
    
    def create(self, validated_data):
        instance = InstitutionSerializer.Meta.model.create(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        InstitutionSerializer.Meta.model.check_duplicate(**validated_data)
        instance.set_institution_name(validated_data.get('institution_name', instance.institution_name))
        instance.set_institution_city(validated_data.get('institution_city', instance.institution_city))
        instance.set_institution_state(validated_data.get('institution_state', instance.institution_state))
        instance.save()
        return instance


class InstitutionYearSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.InstitutionYear
        fields = ['url', 'institution', 'year', 'school_year']

    def create(self, validated_data):
        instance = InstitutionYearSerializer.Meta.model.create(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        InstitutionYearSerializer.Meta.model.check_duplicate(**validated_data)
        instance.set_institution_year(validated_data.get('year', instance.year))
        instance.save()
        return instance

class InstitutionYearProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.InstitutionYearProfile
        fields = ['url', 'yearbook_user', 'institution_year', 'is_educator']

    def create(self, validated_data):
        instance = InstitutionYearProfileSerializer.Meta.model.create(**validated_data)
        instance.save()
        return instance


class SignatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Signature
        fields = ['url', 'author', 'recipient', 'signature']

    def create(self, validated_data):
        instance = SignatureSerializer.Meta.model.create(**validated_data)
        instance.save()
        return instance

