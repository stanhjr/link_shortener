from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


error_messages = {
    'required': 'This field is required',
    'caps': 'This field if case sensitive'
}


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username",
                               max_length=50,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control item',
                                       'placeholder': 'Username',
                                       'id': 'username'

                                   }
                               ))
    password = forms.CharField(label="Password confirmation",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control item',
                                       'placeholder': 'Password',
                                       'id': 'password'
                                   }
                               ))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError(message='username or password fields does not match')
