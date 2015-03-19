from django.db import models

from models.Comic import Comic

class ComicSubscription(models.Model):

    TYPE_ONGOING = 'GO'
    TYPE_ONETIME = 'NT'
    SUBSCRIPTION_TYPE_CHOICES = (
        (TYPE_ONGOING, 'ongoing'),
        (TYPE_ONETIME, 'onetime')
    )

    comic = models.ForeignKey(Comic, related_name='subscriptions')
    issue = models.BooleanField(default=False)
    trade = models.BooleanField(default=False)
    hardcover = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True)
    subscription_type = models.CharField(choices=SUBSCRIPTION_TYPE_CHOICES, max_length=2, default=TYPE_ONGOING)
