from django.test import TestCase


from shortener.models import Links
from users.models import CustomUser


class ShortenerModelTest(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.user = CustomUser.objects.filter(username='admin').first()
        self.initial_link_obj = Links.get_or_create(long_url='https://docs.djangoproject.com/', user=self.user)
        self.long_url = 'https://github.com/'

    def test_link_create(self):
        links_obj = Links.get_or_create(long_url=self.long_url, user=self.user)
        self.assertEquals(links_obj.long_url, 'https://github.com/')

    def test_link_str(self):
        links_obj = Links.get_or_create(long_url='https://docs.djangoproject.com/', user=self.user)
        links_obj_2 = Links.get_or_create(long_url='https://docs.djangoproject.com/', user=self.user)
        self.assertEquals(str(links_obj), str(links_obj_2))

    def test_create_shortened_url(self):
        shortened_url = Links.create_shortened_url()
        self.assertNotEqual('Es23E35', shortened_url)
