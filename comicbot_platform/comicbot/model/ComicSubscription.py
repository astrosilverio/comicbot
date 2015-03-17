from django.db import models

from models.Comic import Comic

class ComicSubscription(models.Model):

    comic = models.ForeignKey(Comic, related_name='subscriptions')
    issue = models.BooleanField('issue', default=False)
    trade = models.BooleanField('trade', default=False)
    hardcover = models.BooleanField('hardcover', default=False)

