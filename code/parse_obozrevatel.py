import datetime

import pandas as pd
import requests
from lxml import html

from code.usr_functions import leave_list, get_dates, unlist_nested, plot_count_day, months24


def parse_obozrevatel(keyword, save_big_csv=1, save_small_csv=1, save_all_and_plot=1):
    titles = []
    dates = []
    now, to = get_dates()
    curr_date = now

    page = requests.get('https://www.obozrevatel.com/ukr/search/?q=' + keyword)
    tree = html.fromstring(page.content)
    title = tree.xpath('//a[@class="news-title-img-text__title"]/text()')
    date = tree.xpath('//time[@class="news-title-img-text__date"]/text()')
    curr_year = datetime.datetime.now().year
    for i in range(len(date)):
        date[i] = date[i][:-7]
        splt = date[i].split()
        splt[1] = months24[splt[1]]
        date[i] = datetime.date(curr_year, int(splt[1]), int(splt[0]))

    titles.append(title)
    dates.append(date)

    j = 2
    while curr_date > to:
        current_month = 0
        previous_month = 0
        page = requests.get('https://www.obozrevatel.com/ukr/search/p' + str(j) + '.htm?q=' + keyword)
        tree = html.fromstring(page.content)
        title = tree.xpath('//a[@class="news-title-img-text__title"]/text()')
        date = tree.xpath('//time[@class="news-title-img-text__date"]/text()')
        titles.append(title)
        dates.append(date)
        curr_date = date[-1]
        curr_year = datetime.datetime.now().year
        for i in range(len(date)):
            previous_month = current_month
            date[i] = date[i][:-7]
            splt = date[i].split()
            splt[1] = months24[splt[1]]
            current_month = int(splt[1])
            if (current_month == 12) and (previous_month == 1):  # можива ситуація коли новини виходять рідко!!!!!
                curr_year -= 1
            date[i] = datetime.date(curr_year, int(splt[1]), int(splt[0]))

        curr_date = date[-1]
        j += 1

    dates = unlist_nested(dates)
    titles = unlist_nested(titles)

    dates = leave_list(dates, to)
    titles = titles[:len(dates)]

    fullDF = pd.DataFrame(
        {'title': titles,
         'date': dates,
         })

    if save_big_csv == 1:
        fullDF.to_csv('saved_data/oboz_big_df.csv', index=False)

    if save_small_csv == 1:
        lightDF = fullDF.groupby('date').count()
        lightDF.to_csv('saved_data/oboz_light_df.csv')

    if save_all_and_plot == 1:
        dftom = pd.read_csv('saved_data/oboz_light_df.csv')
        alldays = []
        step = datetime.timedelta(days=1)
        while to <= now:
            alldays.append(to)
            to += step
        toVis = pd.DataFrame(
            {'date': alldays,
             })

        toVis['date'] = toVis['date'].astype('datetime64[ns]')
        dftom['date'] = dftom['date'].astype('datetime64[ns]')
        dftom['title'] = dftom['title'].astype('int')
        toVis = toVis.merge(dftom, how='left')
        toVis = toVis.fillna(0)
        toVis.to_csv('saved_data/oboz_light_df_all_dates.csv', index=False)

        plot_count_day(alldays, toVis['title'], name='OBOZREVATEL')
        print('obozrevatel WAS PARSED')

    return 0
