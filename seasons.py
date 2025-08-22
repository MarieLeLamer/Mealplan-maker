from datetime import date, datetime

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('Hiver', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('Printemps', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('Été', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('Automne', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('Hiver', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season():
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)
