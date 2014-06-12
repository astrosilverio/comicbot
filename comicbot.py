import urllib2
import datetime
import time
import sys
import re
from bs4 import BeautifulSoup
from collections import defaultdict


class CLDBotError(Exception):
    pass

class CLDBot(object):

    current_week_url = 'http://www.comiclist.com'
    next_week_url = 'http://www.comiclist.com/index.php/newreleases/next-week'
    ignores = ['to', 'in', 'if', 'get', 'week', 'for', 'this', 'and', 'or', 'print']
    command_words = ['next', 'add', 'remove','predict','future','pull', 'check']
    
    def __init__(self, pull_list):
        self.pull_list = self.make_pull_list(pull_list)
        self.today = datetime.date.today()
        self.this_weds = self.get_weds(self.today)
        m_d_y = self.make_m_d_y(self.this_weds)
        self.futures = {'Marvel': 'http://www.comiclist.com/index.php/lists/marvel-comics-extended-forecast-for-'+m_d_y,
                'DC':'http://www.comiclist.com/index.php/lists/dc-comics-extended-forecast-for-'+m_d_y, 
                'Image': 'http://www.comiclist.com/index.php/lists/image-comics-extended-forecast-for-'+m_d_y,
                'BOOM': 'http://www.comiclist.com/index.php/lists/boom-studios-extended-forecast-for-'+m_d_y,
                'Dark Horse': 'http://www.comiclist.com/index.php/lists/dark-horse-comics-extended-forecast-for-'+m_d_y
                }
        self.soups = {self.this_weds: self.make_soup(self.current_week_url), self.this_weds+datetime.timedelta(days=7): self.make_soup(self.next_week_url)}
        self.queries = {'next': self.next_week, 'add': self.add_to_pull, 'remove': self.remove_from_pull, 'future': self.predict, 'check': self.this_week, 'pull': self.print_pull}

    def make_pull_list(self, pull_file):
        '''only relevant when CLDBot is instantiated'''
        with open(pull_file) as pull:
            books = pull.readlines()
        books = [book.rstrip('\n') for book in books]
        return books

    def get_weds(self, day):
        '''returns the Wednesday of the week starting with Monday; I'm assuming that ComicList updates every Monday, which is historically the case.
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

    def make_m_d_y(self, weds):
        month = weds.month
        day = weds.day
        year = str(weds.year)

        if month < 10:
            month = '0'+str(month)
        else:
            month = str(month)
        if day < 10:
            day = '0'+str(day)
        else:
            day = str(day)

        m_d_y = '-'.join([month, day, year])
        return m_d_y

    def make_soup(self, url_of_html):
        '''not super necessary but the urllib stuff is a pain to type'''
        soup = BeautifulSoup(urllib2.urlopen(url_of_html).read())
        return soup

    def check_soup(self, soup, titles=None):
        ''' For current and next weeks, all the comics are links,
        so search for links'''
        if not titles:
            titles = self.pull_list
        my_books = defaultdict(list)
        for name in titles:
            for link in soup.find_all('a'):
                if name in link.get_text():
                    variant = re.findall('\([^()]+\)', link.get_text())
                    if len(variant) == 0:
                        issue = link.get_text()
                        my_books[issue]
                    else:
                        issue = re.sub('\([^()]+\)', '', link.get_text()).rstrip()
                        issue = ' '.join([issue] + variant[:-1])
                        variant = variant[-1]
                        my_books[issue].append(variant)
        return my_books
        
    def check_future_soup(self, soup, titles=None):
        '''for future predictions, data is in table, not a list of links'''
        if not titles:
            titles = self.pull_list
        my_books = defaultdict(lambda: defaultdict(list))
        for name in titles:
            for link in soup.find_all('a'):
                if name in link.get_text():
                    strdate = str(link.parent.parent.contents[1].contents[0])
                    try:
                        middate = time.strptime(strdate, '%m/%d/%y')
                        date = str(datetime.date(middate.tm_year, middate.tm_mon, middate.tm_mday))
                    except ValueError:
                        date = strdate
                    variant = re.findall('\([^()]+\)', link.get_text())
                    if len(variant) == 0:
                        issue = link.get_text()
                        # if there aren't variants, make an empty list
                        my_books[date][issue]
                    else:
                        issue = re.sub('\([^()]+\)', '', link.get_text()).rstrip()
                        issue = ' '.join([issue] + variant[:-1])
                        variant = variant[-1]
                        my_books[date][issue].append(variant)
        return my_books

    def make_future_soups(self):
        '''make soups for predictions pages'''
        future_soups = {}
        for publisher, url in self.futures.iteritems():
            try:
                future_soups[publisher] = self.make_soup(url)
            except HTTPError:
                print "Couldn't make soup for "+publisher
                print url
        return future_soups

    def print_books_per_day(self, date, books):
        '''turns a dictionary of titles into a string'''
        book_entries = []
        for issue, variants in books.iteritems():
            if len(variants) > 1:
                variants = ['\t'+variant for variant in variants]
                book_entry = '\n'.join([issue]+variants)
            elif len(variants) == 1:
                book_entry = ' '.join([issue]+variants)
            else:
                book_entry = issue
            book_entries.append(book_entry)
        book_entries.append('\n')
        books_out = '\n'.join(book_entries)
        intro = "On {0}, the following titles are coming out:".format(date)
        out = '\n\n'.join([intro, books_out])
        return out

    def print_pull(self, *titles):
        '''either prints your pull or tells you if certain titles are in your pull'''
        if titles:
            pulled_titles = [title for title in titles if title in self.pull_list]
            intro = "Of those titles, you are currently pulling:"
        else:
            pulled_titles = self.pull_list[:]
            pulled_titles.append('\n')
            intro = "You are currently pulling:"
        pulled = '\n'.join(pulled_titles)
        out = '\n\n'.join([intro, pulled])
        return out

    def this_week(self, *titles):
        '''checks current week's comiclist for titles'''
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
        '''checks next week's comiclist for titles'''
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
        '''checks predictions pages for titles'''
        if not titles:
            titles = None
            publishers = None
        else:
            publishers = [name for name in titles if name in self.futures]
            titles = [name for name in titles if name not in publishers]
        if not publishers:
            publishers = self.futures.keys()
        try:
            self.__getattribute__('future_soups')
        except AttributeError:
            self.future_soups = self.make_future_soups()
        books = defaultdict(lambda: defaultdict(list))
        for pub in publishers:
            new_books = self.check_future_soup(self.future_soups[pub], titles=titles)
            for date, issues in new_books.iteritems():
                books[date].update(issues)
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
        '''adds things to pull list'''
        if titles:
            repeats = [title for title in titles if title in self.pull_list]
            titles = [title for title in titles if title not in self.pull_list]
        if not titles:
            raise CLDBotError("trying to add nothing")
        intro = "The following titles were added to your pull list:"
        added = '\n'.join(titles)
        if repeats:
            repeat_intro = "The following titles were already in your pull list:"
            not_added = '\n'.join(repeats)
            out = '\n\n'.join([intro, added, repeat_intro, not_added])
        else:
            out = '\n\n'.join([intro, added])
        self.pull_list.extend(titles)
        return out
        
    def remove_from_pull(self, *titles):
        '''removes things from pull list'''
        if not titles:
            raise CLDBotError("nothing to remove")
        if titles:
            to_remove = [title for title in titles if title in self.pull_list]
            not_in_pull = [title for title in titles if title not in self.pull_list]
        intro = "The following titles were removed from your pull list:"
        removed = '\n'.join(to_remove)
        if not_in_pull:
            not_found_intro = "The following titles are not in your pull list:"
            not_found = '\n'.join(not_in_pull)
            out = '\n\n'.join([intro, removed, not_found_intro, not_found])
        else:
            out = '\n\n'.join([intro, removed])
        for title in to_remove:
            self.pull_list.remove(title)
        return out

    def process(self, user_input):
        '''attempts to process user input'''
        words = user_input.split()
        command = words[0]
        titles = words[1:]
        titles = [word.lstrip().rstrip().title() for word in ' '.join(titles).split(',') if word]
        try:
            if command not in self.queries:
                raise CLDBotError('no recognizable command')
            print "success"
            print command, titles
            result = self.queries[command](*titles)
        except CLDBotError as exc:
            print "error"
            result = exc.args[0]
        finally:
            return result

def main(pull_list_file):
    '''main loop'''
    comics_jarvis = CLDBot(pull_list_file)
    running = True
    while running:
        user_input = raw_input('> ')
        if user_input == 'quit':
            running = False
        output = comics_jarvis.process(user_input)
        if output:
            print output
            
if __name__ == '__main__':
    try:
        pull_list_file = sys.argv[1]
    except IndexError:
        pull_list_file = raw_input("You need to give me a pull list. Filename? ")
    main(pull_list_file)
