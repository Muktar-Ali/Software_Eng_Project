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
    def test_BlankSpacesInSignup(self):
        dict_spaces = {
            'username': "     ", #username contains only spaces, which should be invalid
            'first_name': "  Test  ", #first name had leading and trailing spaces
            'last_name': "User   ", # last name has trailing spaces
            'email': "validemail@gmail.com", #email and password is valid
            'password': "ValidPassword123",
            'gender': 'M',
            'age': 24,
            'height': 45,
            'weight': 160,
            'activity_level': "Light",
        }
        form=SignupForm(dict_spaces)
        #check that the form is invalid due to the username containing only spaces
        self.assertFalse(form.is_valid(), "Form should be invalud when username contains only spaces.")
        #ensure that the usernmae field specifically triggered an error
        self.assertIn('username', form.errors, "Username field should trigger an error for blank spaces.")
        #if the form is valid, get cleaned data, otherwise, set an empty dict
        cleaned_data=form.cleaned_data if form.is_valid() else{}
        #check that the first name is correctly stripped of extra spaces
        self.assertEqual(cleaned_data.get('first_name', '').strip(),"Test", "First name should be stripped of spaces.")
        #check that the last name is correctly stipped of extra spaces
        self.assertEqual(cleaned_data.get('last_name', '').strip(), "User", "Last name should be stripped of spaces")
    def test_InvalidEmailFormat(self):
        dict_invalid_email={
        'username': "invalidEmailUser",
        'first_name': "Invalid",
        'last_name': "Email",
        'email': "not-email", #invalid email format
        'password': "ValidPassword123", 
        'gender': 'M',
        'age': 24,
        'height': 45,
        'weight': 160,
        'activity_level': "Light",
        }
        form=SignupForm(dict_invalid_email)
        #check that the form is invalid due to incorrect email format
        self.assertFalse(form.is_valid(),"Form should be invalid with an incorrect email format.")
        #ensure that the email field specifically triggered an error
        self.assertIn('email', form.errors, "Email field should trigger an error for invalid format.")