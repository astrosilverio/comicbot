import datetime

def get_wednesday(day=None):
    """Returns the closest Wednesday
    """
    if not day:
        day = datetime.date.today()
    if type(day) != datetime.date:
        raise Exception("Expecting a datetime object.")
    day_of_week = day.weekday()
    if day_of_week == 2:
        return day
    else:
        delta = 2 - day_of_week
        weds = day + datetime.timedelta(days=delta)
        return weds

def format_comics(comics):
    output = ''
    pubs = sorted(comics.keys())
    for pub in pubs:
        output = output + format_single_publisher(pub.title(), sorted(comics[pub])) + '\n\n'
    return output

def format_single_publisher(publisher, names):
    single_line_out = '\t{}'
    names_out = '\n'.join([single_line_out.format(name.title()) for name in names])
    return '{0}:\n{1}'.format(publisher, names_out)
