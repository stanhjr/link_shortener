from django.test import TestCase

from shortener.models import Links


class ShortenerModelTest(TestCase):

    def setUp(self):
        self.long_url = 'https://github.com/'

    def test_link_create(self):
        links_obj, created = Links.objects.get_or_create(long_url=self.long_url)
        self.assertEquals(links_obj.long_url, 'https://github.com/')

    def test_link_str(self):
        links_obj, created = Links.objects.get_or_create(long_url='https://docs.djangoproject.com/')
        links_obj_2, created = Links.objects.get_or_create(long_url='https://docs.djangoproject.com/')
        self.assertEquals(str(links_obj), str(links_obj_2))

    def test_create_shortened_url(self):
        shortened_url = Links.create_shortened_url()
        self.assertNotEqual('Es23E35', shortened_url)

    def test_unique_model(self):
        links_obj, created = Links.objects.get_or_create(long_url='https://docs.djangoproject.com/en/4.1/ref/models/')
        links_obj_2, created = Links.objects.get_or_create(long_url='https://docs.djangoproject.com/en/4.1/ref/models/')
        self.assertEquals(links_obj.pk, links_obj_2.pk)