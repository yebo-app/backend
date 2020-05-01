from django.test import TestCase
from .models import *
# Create your tests here.

class YearbookUserTests(TestCase):
    #TODO: figure out how to run this test case without submitting a 2nd argument
    def test_user_created_with_default_bio(self):
        new_user= User(username= "test_case", first_name= "test", last_name= "case")
        new_yearbook_user= YearbookUser.create(new_user, "")
        self.assertIs(new_yearbook_user.get_user_bio(), "")

class InstitutionTests(TestCase):
    def test_check_duplicates(self):
        name= "testname"
        city= "testcity"
        state= "teststate"
        test_object= Institution.create(name, city, state)
        self.assertRaises(Exception, Institution.check_duplicate(name,city,state))

    def test_duplicate_create(self):
        name= "testname"
        city= "testcity"
        state= "teststate"
        test_object= Institution.create(name, city, state)
        self.assertRaises(Exception, Institution.create(name,city,state))

    '''def test_set_institution_name(self):
        name= "testname"
        city= "testcity"
        state= "teststate"
        test_object= Institution.create(name, city, state)
        self.assertRaises(Exception, Institution.set_institution_name(name,city,state))
        '''

