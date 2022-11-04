from django.db import models

from shortener.tools import create_random_code


class Links(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)

    def __str__(self):
        return f'{self.long_url} -> {self.short_url}'

    @classmethod
    def create_shortened_url(cls) -> str:
        random_code = create_random_code()
        if cls.objects.filter(short_url=random_code).exists():
            return cls.create_shortened_url()
        return random_code

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = Links.create_shortened_url()
        super(Links, self).save(*args, **kwargs)


