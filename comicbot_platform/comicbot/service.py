def get_releases_for_date(after_date=None, before_date=None):
    if not after_date and not before_date:
        after_date = get_wednesday(datetime.date.today())
        before_date = after_date + datetime.timedelta(days=1)
    if not before_date:
        before_date = get_wednesday(datetime.date.today())
    if not after_date:


def get_recent_releases_for_user(user, after_date=None, before_date=None):
    if not after_date:
        after_date = get_wednesday(datetime.date.today())
    if not before_date:
        before_date = after_date
    query = user.subscriptions.filter()


def check_recent_releases(comics=None, publishers=None, after_date=None, before_date=None, format=None):
    if not after_date:
        after_date = get_wednesday(datetime.date.today())
    if not before_date:
        before_date = after_date
    query = self.subscriptions.filter(comic__recent_releases__release_date__range=(after_date, before_date))
    if comics:
        query = query.filter(comic__name__in=comics)
    if publishers:
        query = query.filter(comic__publisher__in=publishers)
    if format:
        query = query.filter()

    results = defaultdict(list)

    for comic in [sub.comic for sub in query]:
        results[comic.publisher].append(comic.name)

    return results
