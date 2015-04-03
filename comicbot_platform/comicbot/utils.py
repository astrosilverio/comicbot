import datetime

def get_wednesday(day=None):
    """Returns the closest Wednesday
    """
    if type(day) != datetime.date:
        raise Exception("Expecting a datetime object.")
    day_of_week = day.weekday()
    if day_of_week == 2:
        return day
    else:
        delta = 2 - day_of_week
        weds = day + datetime.timedelta(days=delta)
        return weds