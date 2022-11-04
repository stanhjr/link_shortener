from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView

from shortener.forms import ShortenerForm
from shortener.models import Links


class IndexCreateView(CreateView):
    template_name = 'index.html'
    login_url = reverse_lazy('login')
    form_class = ShortenerForm

    def form_valid(self, form):
        context = {}
        links_obj, created = Links.objects.get_or_create(long_url=form.cleaned_data.get('long_url'))
        context['new_url'] = self.request.build_absolute_uri('/') + links_obj.short_url,
        context['long_url'] = links_obj.long_url
        context['click_counter'] = self.request.session.get(links_obj.short_url)
        return render(self.request, self.template_name, context)


def redirect_url_view(request, shortened_part):
    links_obj = Links.objects.filter(short_url=shortened_part).first()
    if not links_obj:
        raise Http404('Sorry this link is broken :(')
    if request.session.get(shortened_part):
        request.session[shortened_part] += 1
    else:
        request.session[shortened_part] = 1

    return HttpResponseRedirect(links_obj.long_url)


