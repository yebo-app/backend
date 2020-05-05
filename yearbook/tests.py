from django.test import TestCase
from .models import *
# Create your tests here.

class YearbookUserTests(TestCase):
    def test_check_static_duplicates(self):
        test_user = User(username="test_case", first_name="test", last_name="case")
        test_yearbook_user = YearbookUser.create(test_user)
        self.assertRaises(Exception, YearbookUser.create(test_user))

    def test_user_created_with_default_bio(self):
        test_user = User(username="test_case", first_name="test", last_name="case")
        test_yearbook_user = YearbookUser.create(test_user)
        self.assertIs(test_yearbook_user.bio, "")

class InstitutionTests(TestCase):
    def test_check_static_duplicates(self):
        name = "testname"
        city = "testcity"
        state = "teststate"
        test_institution = Institution.create(name, city, state)
        self.assertRaises(Exception, Institution.check_duplicate(name, city, state))

    def test_duplicate_create(self):
        name = "testname"
        city = "testcity"
        state = "teststate"
        test_institution = Institution.create(name, city, state)
        self.assertRaises(Exception, Institution.create(name,city,state))

    def test_set_institution_name(self):
        name = "testname"
        city = "testcity"
        state = "teststate"
        name2 = "testname2"
        test_institution = Institution.create(name, city, state)
        test_institution_2 = Institution.create(name2, city, state)
        self.assertRaises(Exception, test_institution_2.set_institution_name(name))

    def test_set_institution_location(self):
        name = "testname"
        city = "testcity"
        state = "teststate"
        city2 = "testcity2"
        test_institution = Institution.create(name, city, state)
        test_institution_2 = Institution.create(name, city2, state)
        self.assertRaises(Exception, test_institution_2.set_institution_location(city,state))

class InstitutionYearTests(TestCase):
    def test_check_static_duplicates(self):
        test_institution = Institution.create("Institution Name")
        test_institution_year = InstitutionYear.create(test_institution, 2020)
        self.assertRaises(Exception, InstitutionYear.create(test_institution, 2020))

class InstitutionYearProfileTests(TestCase):
    def test_check_static_duplicates(self):
        test_user = User(username="test_case", first_name="test", last_name="case")
        test_yearbook_user = YearbookUser.create(test_user)
        test_institution = Institution.create("Institution Name")
        test_institution_year = InstitutionYear.create(test_institution, 2020)
        test_institution_year_profile = InstitutionYearProfile.create(test_yearbook_user, test_institution_year, False)
        self.assertRaises(Exception, InstitutionYearProfile.create(test_yearbook_user, test_institution_year))

class SignatureTests(TestCase):
    def test_check_signature_created_with_default_value(self):
        test_user = User(username="test_case", first_name="test", last_name="case")
        test_yearbook_user = YearbookUser.create(test_user)
        test_institution = Institution.create("Institution Name")
        test_institution_year = InstitutionYear.create(test_institution, 2020)
        test_institution_year_profile = InstitutionYearProfile.create(test_yearbook_user, test_institution_year, False)
        test_signature = Signature.create(test_yearbook_user, test_institution_year_profile)
        self.assertIs(test_signature.signature, "")
