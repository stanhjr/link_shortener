from django.test import TestCase

from shortener.forms import ShortenerForm


class ShortenerFormTest(TestCase):

    def test_enter_long_url_valid(self):
        form_data = {'long_url': 'https://github.com/', }
        form = ShortenerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_enter_long_url_not_valid(self):
        form_data = {'long_url': 'StanHall', }
        form = ShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())
