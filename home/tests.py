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
    def test_DuplicateUsernameTest(self):
    # Create a user first
        dict = {
        'username': "duplicateUser",
        'first_name': "Duplicate",
        'last_name': "User",
        'email': "duplicate@gmail.com",
        'password': "DuplicateUser123",
        'gender': 'M',
        'age': 30,
        'height': 68,
        'weight': 160,
        'activity_level': "Heavy",
         }
        form = SignupForm(dict)
        form.save()  # First save should work
        # Try creating another user with the same username
        duplicate_data = dict.copy()
        duplicate_data['username'] = "duplicateUser"  # Change email to avoid duplicate email error
        duplicate_form = SignupForm(duplicate_data)
        self.assertFalse(duplicate_form.is_valid())  # Should fail due to duplicate username
    def test_UserProfileUpdateTest(self):
        user_data = {
            'username': "updateUser",
            'first_name': "Update",
            'last_name': "User",
            'email': "updateuser@gmail.com",
            'password': "UpdateUser123",
            'gender': 'M',
            'age': 35,
            'height': 70,
            'weight': 180,
            'activity_level': "Heavy",
        }
        form = SignupForm(user_data)
        form.save()
        # Login and update profile
        self.client.login(username="updateUser", password="UpdateUser123")
        updated_data = {'first_name': "Updated", 'age': 36}
        response = self.client.post('/profile/update/', updated_data)  # Adjust URL as needed
        user = CustomUser.objects.get(username="updateUser")
        self.assertEqual(user.first_name, "Update")  # Check if update was successful
    def test_InvalidLoginTest(self):
        user_data = {
            'username': "validUser",
            'first_name': "Valid",
            'last_name': "User",
            'email': "validuser@gmail.com",
            'password': "ValidPassword123",
            'gender': 'F',
            'age': 28,
            'height': 64,
            'weight': 130,
            'activity_level': "Light",
        }
        form = SignupForm(user_data)
        form.save()
        # Try logging in with wrong password
        self.assertFalse(self.client.login(username="validUser", password="WrongPassword"))
    
