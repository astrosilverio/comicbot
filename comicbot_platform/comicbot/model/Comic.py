from django.db import models

class Comic(models.Model):

    name = models.CharField(max_length=128, null=False)
    publisher = models.CharField(max_length=32, null=False)