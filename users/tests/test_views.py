from django.test import TestCase, RequestFactory, Client

from django.urls import reverse_lazy

from users.models import CustomUser


class UsersViewsTest(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.filter(username='admin').first()

    def test_login(self):
        c = Client()
        response = c.post(reverse_lazy('login'), {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('index'))

    def test_login_not_valid(self):
        c = Client()
        response = c.post(reverse_lazy('login'), {'username': 'admin2', 'password': 'admin'})
        self.assertEqual(response.url, reverse_lazy('login'))
