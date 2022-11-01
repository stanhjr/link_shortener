from django.urls import path

from shortener import views


urlpatterns = [
    path('', views.IndexCreateView.as_view(), name='index'),
    path('<str:shortened_part>', views.redirect_url_view, name='redirect')

]