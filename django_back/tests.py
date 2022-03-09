from django.test import TestCase
from django.test import Client
from api.models import User

# Create your tests here.


class AuthTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", email="test@email.com")
        user.set_password('pass')
        user.save()

    def test_register_login(self):
        """Users can register and login to access data"""
        client = Client(enforce_csrf_checks=True)
        response = client.get('/auth/users/', {'username': 'testuser', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 401)

        response = client.post('/auth/users/', {'username': 'testuser', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 400)

        response = client.post('/auth/users/', {'username': 'testuser2', 'email': 'test@email.com'})
        self.assertEqual( response.status_code, 400)
        
        response = client.post('/auth/users/', {'username': 'testuser2', 'email': 'test@email.com', 'password':'pass'})
        self.assertEqual( response.status_code, 400)

        response = client.post('/auth/users/', {'username': 'testuser2', 'email': 'test@email.com', 'password':'pass12029'})
        self.assertEqual( response.status_code, 201)
        self.assertEqual( response.json()['email'], 'test@email.com')
        self.assertEqual( response.json()['username'], 'testuser2')
        self.assertEqual( response.json()['id'], 2)

        response = client.get('/auth/token/login/')
        self.assertEqual( response.status_code, 405)

        response = client.post('/auth/token/login', {'username': 'testuser2', 'password':'pass2'})
        self.assertEqual( response.status_code, 400)

        response = client.post('/auth/token/login/', {'username': 'testuser2', 'password':'pass12029'})
        self.assertEqual( response.status_code, 200)

        token = response.json()['auth_token']

        response = client.get('/api/v1.0/users', **{'HTTP_AUTHORIZATION':'Token 1' + token})
        self.assertEqual( response.status_code, 401)

        response = client.get('/api/v1.0/users', **{'HTTP_AUTHORIZATION':'Token ' + token})
        self.assertEqual( response.status_code, 200)

        self.assertEqual( response.json()[0]['username'], 'testuser')
        self.assertEqual( response.json()[1]['username'], 'testuser2')
