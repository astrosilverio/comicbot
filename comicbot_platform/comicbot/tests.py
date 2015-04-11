import datetime
from freezegun import freeze_time

from django.test import TestCase
from models import Comic, User, ComicSubscription, Release
from utils import get_wednesday, format_comics, format_single_publisher

# Create your tests here.

def BaseTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = User(username='astrosilverio', email='me@gmail.com', password='ironman')
        self.user.save()

        self.rachel = User(username='magpieohmy', email='rachel@gmail.com', password='thursday')
        self.rachel.save()

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

        ComicSubscription(user=self.rachel, comic=self.comics['ms_marvel'], trades=True).save()
        ComicSubscription(user=self.rachel, comic=self.comics['saga'], issues=False, trades=True).save()
        ComicSubscription(user=self.rachel, comic=self.comics['lumberjanes'], trades=True).save()

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


class TestUtils(TestCase):

    @freeze_time("2015-03-11")
    def test_get_wednesday_on_wednesday(self):
        wednesday = get_wednesday()
        self.assertEqual(wednesday, datetime.date(2015, 3, 11))

    @freeze_time("2015-03-09")
    def test_get_wednesday_before_wednesday(self):
        wednesday = get_wednesday()
        self.assertEqual(wednesday, datetime.date(2015, 3, 11))

    @freeze_time("2015-03-13")
    def test_get_wednesday_after_wednesday(self):
        wednesday = get_wednesday()
        self.assertEqual(wednesday, datetime.date(2015, 3, 11))


# class CheckRecentReleasesTest(BaseTest):

#     @
#     def test_with_just_user(self):
#         results = self.user.check_recent_releases()