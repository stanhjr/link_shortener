from django.test import TestCase


from users.forms import LoginForm


class ShortenerFormTest(TestCase):
    fixtures = ['initial_data.json', ]

    def test_login_form_valid(self):
        form_data = {'username': 'admin', 'password': 'admin'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_not_valid(self):
        form_data = {'username': 'admin1', 'password': 'admin'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


