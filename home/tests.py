from django.test import TestCase
from users.models import CustomUser
from users.forms import SignupForm

# Create your tests here.
class UserTestCase(TestCase):
    def test_SignUpTest(self):
        dict = {
            'username':"testUser",
            'first_name':"Testing",
            'last_name':"User",
            "email":"thetestuser@gmail.com",
            'password':"BestTestUser",
            'gender':'O',
            'age':25,
            'height':71,
            'weight':138,
            'activity_level':"Light",   
        }
        form = SignupForm(dict)
        form.save()
        CustomUser.objects.get(username=dict['username'])
    def test_LoginTest(self):
        dict = {
            'username':"anotherTestUser",
            'first_name':"Also",
            'last_name':"Testing",
            "email":"nexttestuser@gmail.com",
            'password':"NextBestTestUser",
            'gender':'O',
            'age':23,
            'height':72,
            'weight':139,
            'activity_level':"Sedentary", 
        }
        form = SignupForm(dict)
        form.save()
        self.assertTrue(self.client.login(username="anotherTestUser", password="NextBestTestUser"))
    def test_LogoutTest(self):
        dict = {
            'username':"ThirdTestUser",
            'first_name':"Third",
            'last_name':"Word",
            "email":"threetestuser@gmail.com",
            'password':"ThreeTestUser",
            'gender':'O',
            'age':22,
            'height':71,
            'weight':133,
            'activity_level':"Sedentary", 
        }
        form = SignupForm(dict)
        form.save()
        self.client.login(username="ThirdTestUser", password="ThreeTestUser")
        self.client.logout()
    
