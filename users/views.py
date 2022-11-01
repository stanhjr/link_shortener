from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


from users.forms import LoginForm


class Login(LoginView):
    success_url = reverse_lazy('index')
    form_class = LoginForm
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'username or password fields does not match')
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.user)
        return HttpResponseRedirect(reverse_lazy('index'))
