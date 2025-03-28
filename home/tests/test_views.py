from django.test import TestCase, Client
from django.urls import reverse
from users.forms import SignupForm


class TestAllViews(TestCase):

    def test_login(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home/login.html')
    

    def test_register(self):
        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home/register.html')
    

    def test_welcome(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home/welcome.html')