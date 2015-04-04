import datetime

from django.test import TestCase
from models import Comic, User, ComicSubscription, Release

# Create your tests here.

def BaseTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = User(username='astrosilverio', email='astrosilverio@gmail.com', password='ironman')
        self.user.save()

        self.comics = {
            'batman': Comic(name='batman', publisher='dc'),
            'wonder_woman': Comic(name='wonder woman', publisher='dc'),
            'ms_marvel': Comic(name='ms. marvel', publisher='marvel'),
            'captain_marvel': Comic(name='captain marvel', publisher='marvel'),
            'lumberjanes': Comic(name='lumberjanes', publisher='boom'),
            'saga': Comic(name='saga', publisher='image'),
            'wicdiv': Comic(name='the wicked + the divine', publisher='image')
        }

        for comic in self.comics.values():
            comic.save()

        ComicSubscription(user=self.user, comic=self.comics['wicdiv'], trades=True).save()
        ComicSubscription(user=self.user, comic=self.comics['ms_marvel']).save()
        ComicSubscription(user=self.user, comic=self.comics['lumberjanes']).save()

        week_one = datetime.datetime(2015, 3, 4)
        week_two = datetime.datetime(2015, 3, 11)
        week_three = datetime.datetime(2015, 3, 18)
        week_four = datetime.datetime(2015, 3, 25)
        week_five = datetime.datetime(2015, 4, 1)

        Release(comic=self.comics['batman'], release_date=week_one).save()
        Release(comic=self.comics['batman'], release_date=week_five).save()
        Release(comic=self.comics['wonder_woman'], release_date=week_two).save()
        Release(comic=self.comics['ms_marvel'], release_date=week_two).save()
        Release(comic=self.comics['captain marvel'], release_date=week_four).save()
        Release(comic=self.comics['lumberjanes'], release_date=week_three).save()
        Release(comic=self.comics['saga'], release_date=week_two).save()
        Release(comic=self.comics['saga'], release_date=week_five).save()
        Release(comic=self.comics['wicdiv'], release_date=week_three).save()

