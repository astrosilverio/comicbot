from collections import defaultdict
import datetime

from django.db import models

import constants
from utils import get_wednesday


class Comic(models.Model):

    class Meta:
        app_label = 'comicbot'

    name = models.CharField(db_index=True, max_length=128, null=False)
    publisher = models.CharField(db_index=True, max_length=32, null=False)

    def __str__(self):
        return "{name} ({publisher})".format(name=self.name, publisher=self.publisher)


class User(models.Model):

    class Meta:
        app_label = 'comicbot'

    username = models.CharField(db_index=True, max_length=32, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.CharField(db_index=True, max_length=64, null=True)

    def __str__(self):
        return self.username


class ComicSubscription(models.Model):

    class Meta:
        app_label = 'comicbot'

    SUBSCRIPTION_TYPE_CHOICES = (
        (constants.SUBSCRIPTION_TYPE_ONGOING, 'ongoing'),
        (constants.SUBSCRIPTION_TYPE_ONETIME, 'onetime')
    )

    VARIANT_PREF_CHOICES = (
        (constants.COVER_TYPE_REGULAR, 'regular'),
        (constants.COVER_TYPE_VARIANT, 'variant'),
        (constants.COVER_TYPE_BOTH, 'both')
    )

    user = models.ForeignKey(User, related_name='subscriptions')
    comic = models.ForeignKey(Comic, related_name='subscriptions')
    issue = models.BooleanField(default=True)
    trade = models.BooleanField(default=False)
    hardcover = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True)
    subscription_type = models.CharField(choices=SUBSCRIPTION_TYPE_CHOICES, max_length=64, default=constants.SUBSCRIPTION_TYPE_ONGOING)
    variant_pref = models.CharField(choices=VARIANT_PREF_CHOICES, max_length=64, default=constants.COVER_TYPE_BOTH)

    def __str__(self):
        return "{user}-{comic}".format(user=self.user.username, comic=self.comic.name)


class Release(models.Model):

    class Meta:
        app_label = 'comicbot'

    RELEASE_TYPE_CHOICES = (
        (constants.RELEASE_TYPE_ISSUE, 'issue'),
        (constants.RELEASE_TYPE_TRADE, 'trade'),
        (constants.RELEASE_TYPE_HARDCOVER, 'hardcover'),
        (constants.RELEASE_TYPE_OTHER, 'other')
    )

    comic = models.ForeignKey(Comic, related_name='recent_releases')
    release_date = models.DateTimeField(null=False, db_index=True, default=get_wednesday)
    release_type = models.CharField(choices=RELEASE_TYPE_CHOICES, default=constants.RELEASE_TYPE_ISSUE)
    variant = models.BooleanField(default=False)

    def __str__(self):
        return "{comic}: {date}".format(comic=self.comic.name, date=self.release_date)
