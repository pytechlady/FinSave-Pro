from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from .models import User

# Create your tests here.

class TestSetup(APITestCase):
    
    def setUp(self):   
        self.register_url=reverse('user-signup')
        self.faker = Faker()
        
        self.user_data={
            'email': self.faker.email(),
            'password': self.faker.password(),
        }
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    

class TestView(TestSetup):
    
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)
        
    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['message'], "User created successfully")

        # Ensure user is created
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.user_data['password']))
        
        
        
    