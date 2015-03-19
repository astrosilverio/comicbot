from django.db import models

class User(models.Model):

    username = models.CharField('username', max_length=32, unique=True, null=False)
    password = models.CharField('password', max_length=128, null=False)
    email = models.CharField('email', max_length=64, null=True)
