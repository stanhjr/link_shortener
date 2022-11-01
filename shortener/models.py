from django.db import models
from users.models import CustomUser

from shortener.tools import create_random_code


class Links(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    users = models.ManyToManyField(CustomUser, related_name='links', through='ClickCounter')

    def __str__(self):
        return f'{self.long_url} -> {self.short_url}'

    @classmethod
    def create_shortened_url(cls):
        random_code = create_random_code()
        if cls.objects.filter(short_url=random_code).exists():
            return cls.create_shortened_url()
        return random_code

    @classmethod
    def get_or_create(cls, long_url: str, user):
        link_obj = cls.objects.filter(long_url=long_url).first()
        shortened_url = cls.create_shortened_url()
        if link_obj and not link_obj.short_url:
            link_obj.short_url = shortened_url
        elif not link_obj:
            link_obj = cls.objects.create(long_url=long_url,
                                          short_url=shortened_url)

        link_obj.users.add(user)
        link_obj.save()
        return link_obj


class ClickCounter(models.Model):
    clicks = models.PositiveIntegerField(default=0)
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    links = models.ForeignKey(Links, on_delete=models.CASCADE)

