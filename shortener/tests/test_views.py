from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser

from shortener.models import Links, ClickCounter
from shortener.views import IndexCreateView
from shortener.views import redirect_url_view
from users.models import CustomUser


class ShortenerViewsTest(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.filter(username='admin').first()
        self.initial_link_obj = Links.get_or_create(long_url='https://docs.djangoproject.com/', user=self.user)

    def test_index_not_login(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = IndexCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/?next=/')

    def test_index_login(self):
        request = self.factory.get('/')
        request.user = self.user
        response = IndexCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_shortened_url(self):
        request = self.factory.post('/', {'long_url': 'https://docs.djangoproject.com/'})
        request.user = self.user
        response = IndexCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_redirect_shortener_status(self):
        request = self.factory.get('/')
        request.user = self.user
        response = redirect_url_view(request, self.initial_link_obj.short_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_shortener_url(self):
        request = self.factory.get('/')
        request.user = self.user
        response = redirect_url_view(request, self.initial_link_obj.short_url)
        self.assertEqual(response.url, 'https://docs.djangoproject.com/')

    def test_check_counter(self):
        check_number = ClickCounter.objects.filter(users=self.user,
                                                   links=self.initial_link_obj).first()
        request = self.factory.get('/' + self.initial_link_obj.short_url)
        request.user = self.user
        redirect_url_view(request, self.initial_link_obj.short_url)
        next_number = ClickCounter.objects.filter(users=self.user,
                                                  links=self.initial_link_obj).first()
        self.assertEqual(1, next_number.clicks - check_number.clicks)
