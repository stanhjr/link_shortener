from django.test import TestCase, Client


from shortener.models import Links


class ShortenerViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.initial_link_obj, create = Links.objects.get_or_create(long_url='https://docs.djangoproject.com/')

    def test_create_shortened_url(self):
        response = self.client.post('/', {'long_url': 'https://docs.djangoproject.com/'})
        self.assertEqual(response.status_code, 200)

    def test_redirect_shortener_status(self):
        response = self.client.post('/' + self.initial_link_obj.short_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_shortener_url(self):
        response = self.client.post('/' + self.initial_link_obj.short_url)
        self.assertEqual(response.url, 'https://docs.djangoproject.com/')

    def test_check_counter(self):
        self.assertEqual(self.client.session.get(self.initial_link_obj.short_url), None)
        self.client.get('/' + self.initial_link_obj.short_url)
        self.assertEqual(self.client.session[self.initial_link_obj.short_url], 1)
        self.client.get('/' + self.initial_link_obj.short_url)
        self.assertEqual(self.client.session[self.initial_link_obj.short_url], 2)
