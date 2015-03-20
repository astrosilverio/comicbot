from django.db import models

class Comic(models.Model):

    class Meta:
        app_label = 'comicbot'

    name = models.CharField(db_index=True, max_length=128, null=False)
    publisher = models.CharField(db_index=True, max_length=32, null=False)

class User(models.Model):

    class Meta:
        app_label = 'comicbot'

    username = models.CharField(db_index=True, max_length=32, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.CharField(db_index=True, max_length=64, null=True)


class ComicSubscription(models.Model):

    class Meta:
        app_label = 'comicbot'

    TYPE_ONGOING = 'GO'
    TYPE_ONETIME = 'NT'
    SUBSCRIPTION_TYPE_CHOICES = (
        (TYPE_ONGOING, 'ongoing'),
        (TYPE_ONETIME, 'onetime')
    )
    COVER_TYPE_REGULAR = 'RG'
    COVER_TYPE_VARIANT = 'VR'
    COVER_TYPE_BOTH = 'BT'
    VARIANT_PREF_CHOICES = (
        (COVER_TYPE_REGULAR, 'regular'),
        (COVER_TYPE_VARIANT, 'variant'),
        (COVER_TYPE_BOTH, 'both')
    )

    user = models.ForeignKey(User, related_name='subscriptions')
    comic = models.ForeignKey(Comic, related_name='subscriptions')
    issue = models.BooleanField(default=True)
    trade = models.BooleanField(default=False)
    hardcover = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True)
    subscription_type = models.CharField(choices=SUBSCRIPTION_TYPE_CHOICES, max_length=2, default=TYPE_ONGOING)
    variant_pref = models.CharField(choices=VARIANT_PREF_CHOICES, max_length=2, default=COVER_TYPE_BOTH)


class Release(models.Model):

    class Meta:
        app_label = 'comicbot'

    comic = models.ForeignKey(Comic, related_name='recent_releases')
    release_date = models.DateTimeField(null=False, db_index=True)
