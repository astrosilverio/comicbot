from django.db import models
from model.Comic import Comic

class Release(models.Model):

    comic = models.ForeignKey(Comic, related_name='recent_releases')
    release_date = models.DateTimeField(null=False)