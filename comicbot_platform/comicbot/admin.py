from django.contrib import admin

# Register your models here.
from comicbot.models import Comic
from comicbot.models import ComicSubscription
from comicbot.models import User
from comicbot.models import Release

admin.site.register(Comic)
admin.site.register(ComicSubscription)
admin.site.register(User)
admin.site.register(Release)
