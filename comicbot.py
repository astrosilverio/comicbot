import urllib2
from bs4 import BeautifulSoup
import datetime
from collections import defaultdict
import time
import pdb

class CLDBotError(Exception):
    pass

class CLDBot(object):

    current_week_url = 'http://www.comiclist.com'
    next_week_url = 'http://www.comiclist.com/index.php/newreleases/next-week'
    futures = {'Marvel': 'http://www.comiclist.com/index.php/lists/marvel-comics-extended-forecast-for-01-08-2014',
'DC':'http://www.comiclist.com/index.php/lists/dc-comics-extended-forecast-for-01-08-2014', 
    'Image': 'http://www.comiclist.com/index.php/lists/image-comics-extended-forecast-for-01-08-2014'}

    def __init__(self, pull_list):
        self.pull_list = self.make_pull_list(pull_list)
        self.today = datetime.date.today()
        self.this_weds = self.get_weds(self.today)
        self.soups = {self.this_weds: self.make_soup(self.current_week_url), self.this_weds+datetime.timedelta(days=7): self.make_soup(self.next_week_url)}

    def make_pull_list(self, pull_file):
        '''only relevant when CLDBot is instantiated'''
        with open(pull_file) as pull:
            books = pull.readlines()
        books = [book.rstrip('\n') for book in books]
        return books

    def get_weds(self, day):
        '''returns the Wednesday of the week starting with Monday; I'm assuming that ComicList updates every Monday, which is historically the case
        assumes that day is a datetime.date object'''
        if type(day) != datetime.date:
            raise CLDBotError("get_weds takes a datetime.date object as input")
        day_of_week = day.weekday()
        if day_of_week == 2:
            return day
        else:
            delta = 2 - day_of_week
            weds = self.today + datetime.timedelta(days=delta)
            return weds

    def make_soup(self, url_of_html):
        '''not super necessary but the urllib stuff is a pain to type'''
        soup = BeautifulSoup(urllib2.urlopen(url_of_html).read())
        return soup

    def check_soup(self, soup, titles=None):
        ''' For current and next weeks, all the comics are links
        e.g. <a href="http://www.shareasale.com/r.cfm?u=167587&amp;b=84187&amp;m=8908&amp;afftrack=special1&amp;urllink=www.tfaw.com/Profile/Halo%3A-Escalation-2___440091%3Fqt%3Dssnrp20140102">Halo Escalation #2</a>'''
        if not titles:
            titles = self.pull_list
        my_books = []
        for name in titles:
            for link in soup.find_all('a'):
                if name in link.get_text():
                    my_books.append(link.get_text())
        return my_books
        
    def check_table_soup(self, soup, titles=None):
        '''for future predictions, data is in table, not a list of links'''
        if not titles:
            titles = self.pull_list
        my_books = defaultdict(list)
        for name in titles:
            for link in soup.find_all('a'):
                if name in link.get_text():
                    strdate = str(link.parent.parent.contents[1].contents[0])
                    try:
                        middate = time.strptime(strdate, '%m/%d/%y')
                        date = str(datetime.date(middate.tm_year, middate.tm_mon, middate.tm_mday))
                    except ValueError:
                        date = strdate
                    my_books[date].append(link.get_text())
        return my_books

    def make_future_soups(self):
        future_soups = {}
        for publisher, url in self.futures.iteritems():
            future_soups[publisher] = self.make_soup(url)
        return future_soups

    def print_books_per_day(self, date, books):
        books.append('\n')
        books_out = '\n'.join(books)
        intro = "On {0}, the following titles are coming out:".format(date)
        out = '\n\n'.join([intro, books_out])
        return out

    def print_pull(self, *titles):
        if titles:
            pulled_titles = [title for title in titles if title in self.pull_list]
            intro = "Of those titles, you are currently pulling:"
        else:
            pulled_titles = self.pull_list.append('\n')
            intro = "You are currently pulling:"
        pulled = '\n'.join(pulled_titles)
        out = '\n\n'.join([intro, pulled])
        return out
        
    def this_week(self, *titles):
        if not titles:
            titles = None
        books = self.check_soup(self.soups[self.this_weds], titles=titles)
        if len(books) == 0:
            return "Nothing is coming out this week for you, sorry!"
        else:
            date = str(self.this_weds)
            out = self.print_books_per_day(date, books)
            return out

    def next_week(self, *titles):
        if not titles:
            titles = None
        books = self.check_soup(self.soups[self.this_weds+datetime.timedelta(days=7)], titles=titles)
        if len(books) == 0:
            return "Nothing is coming out this week for you, sorry!"
        else:
            date = str(self.this_weds+datetime.timedelta(days=7))
            out = self.print_books_per_day(date, books)
            return out
            
    def predict(self, *titles):
        if not titles:
            titles = None
        else:
            publishers = [name for name in titles if name in self.futures]
            titles = [name for name in titles if name not in publishers]
        if not publishers:
            publishers = self.futures.keys()
        try:
            self.__getattribute__('future_soups')
        except AttributeError:
            self.future_soups = self.make_future_soups()
        books = defaultdict(list)
        for pub in publishers:
            new_books = self.check_table_soup(self.future_soups[pub], titles=titles)
            for date, issues in new_books.iteritems():
                books[date].extend(issues)
        if len(books.keys()) == 0:
            return "We can't find predictions for you, sorry!"
        else:
            unsorted = [(date, self.print_books_per_day(date,issues)) for date, issues in books.iteritems()]
            predictions = [book_list for (date, book_list) in sorted(unsorted)]
            body = '\n\n'.join(predictions)
            intro = "Predictions by book. Accuracy not guaranteed!"
            out = '\n\n'.join([intro, body])
            return out
            
    def add_to_pull(self, *titles):
        self.pull_list.extend(titles)
# 
# 
# 
# 
# 
# 
#     def __init__(self, pull_list):
#         self.pull_list = self.make_pull_list(pull_list)
#         self.current_soup = self.make_soup(self.current_week)
#         self.queries = {'current': self.check_soup, 'next': self.check_next_week}
# 
#         print(self)
#         
#     def __str__(self):
#         current_books = self.check_soup(self.current_soup)
#         books = '\n'.join(current_books)
#         return books
#         
# 
#         
# 
#         
# 
#         
#     def check_next_week(self, titles=None):
#         next_soup = self.make_soup(self.next_week)
#         books = self.check_soup(next_soup, titles=titles)
#         return books
#         
#     def check_title(self, title):
#         pass
#         
#     def process(self, user_input):
#         words = user_input.split()
#         command = words[0]
#         args = words[1:]
#         try:
#             result = self.queries[command](*args)
#         except:
#             raise CLDBotError('didnt work')
