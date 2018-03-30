import datetime
from urllib import request

import datedelta
import matplotlib.pyplot as plt


def cyrillic_url(cyr_str):
    return request.quote(cyr_str.encode('cp1251'))


def leave_list(lst, cond):
    to_append = []
    for i in range(len(lst)):
        if lst[i] > cond:
            to_append.append(lst[i])
    return to_append


def get_dates(month_to_parse=3):
    now = (datetime.datetime.now())
    to = (now - month_to_parse * datedelta.MONTH)
    to = to.date()
    now = now.date()
    return now, to


def unlist_nested(lst):
    return [item for sublist in lst for item in sublist]


def plot_count_day(period, count_news, name='UNKNOWN'):
    plt.figure(num=None, figsize=(15, 8))
    plt.plot(period, count_news)
    plt.title(name)
    plt.xticks(period, [str(i) for i in period], rotation='vertical')
    plt.show()


def new_news(new_parsed, old_parsed):
    new = []
    for i in new_parsed:
        if i not in old_parsed:
            new.append(i)
    return new


months24 = {
    'січня': 1,
    'сiчня': 1,
    'лютого': 2,
    'березня': 3,
    'квітня': 4,
    'травня': 5,
    'червня': 6,
    'липня': 7,
    'серпня': 8,
    'вересня': 9,
    'жовтня': 10,
    'листопада': 11,
    'грудня': 12,
}
