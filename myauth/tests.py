import email
from django.test import TestCase
from django.test import Client
from api.models import User

# Create your tests here.


class RegisterTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", email="test@email.com")
        user.set_password('pass')
        user.save()

    def test_register_login(self):
        """Users can register and login to access data"""
        client = Client(enforce_csrf_checks=True)
        response = client.get('/auth/register/', {'username': 'testuser', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 405)

        response = client.post('/auth/register/', {'username': 'testuser', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 400)

        response = client.post('/auth/register/', {'username': 'testuser2', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 400)
        
        response = client.post('/auth/register/', {'username': 'testuser2', 'email': 'test@email.com', 'password':'pass'})
        self.assertEqual( response.status_code, 201)

        response = client.get('/auth/login/')
        self.assertEqual( response.status_code, 405)

        response = client.post('/auth/login/', {'username': 'testuser2', 'password':'pass2'})
        self.assertEqual( response.status_code, 400)

        response = client.post('/auth/login/', {'username': 'testuser2', 'password':'pass'})
        self.assertEqual( response.status_code, 200)

        token = response.json()['token']

        response = client.get('/api/v1.0/users', **{'HTTP_AUTHORIZATION':'Token 1' + token})
        self.assertEqual( response.status_code, 401)

        response = client.get('/api/v1.0/users', **{'HTTP_AUTHORIZATION':'Token ' + token})
        self.assertEqual( response.status_code, 200)

        self.assertEqual( response.json()[0]['username'], 'testuser')
        self.assertEqual( response.json()[1]['username'], 'testuser2')
