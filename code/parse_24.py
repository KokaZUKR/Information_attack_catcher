import datetime

import pandas as pd
import requests
from lxml import html

from code.usr_functions import leave_list, get_dates, unlist_nested, plot_count_day, months24


def parse_24(keyword, save_big_csv=1, save_small_csv=1, save_all_and_plot=1):
    titles = []
    dates = []
    now, to = get_dates()
    curr_date = now

    #  REWRITE THIS LOOP INTO USR_FUNCTIONS!!!!
    #  REWRITE FROM LXML TO BEAUTIFUL SOUP!!!!!
    #  FIX BIDLOCODE

    j = 1
    while curr_date > to:
        print(curr_date, to)
        page = requests.get('https://24tv.ua/search/search.do?searchValue=' + keyword + '&mode=all&relevance=true')
        tree = html.fromstring(page.content)
        title = tree.xpath('//a[@class="news_title"]/text()')
        date = tree.xpath('//span[@class="date_time"]/text()')
        current_year = datetime.datetime.now().year
        current_month = 0
        previous_month = 0
        for i in range(len(date)):
            previous_month = current_month
            date[i] = date[i][:-10]
            if date[i] == 'сьогодні':
                date[i] = datetime.datetime.now().date()
                current_month = datetime.datetime.now().month
            else:
                date_to_process = date[i].split()
                date_to_process[1] = months24[date_to_process[1]]
                current_month = date_to_process[1]
                if (current_month == 12) and (previous_month == 1):  # можива ситуація коли новини виходять рідко!!!!!
                    current_year -= 1
                date[i] = datetime.date(current_year, current_month, int(date_to_process[0]))
        dates.append(date)
        titles.append(title)
        print(date)

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
        fullDF.to_csv('saved_data/24_big_df.csv', index=False)

    if save_small_csv == 1:
        lightDF = fullDF.groupby('date').count()
        lightDF.to_csv('saved_data/24_light_df.csv')

    if save_all_and_plot == 1:
        dftom = pd.read_csv('saved_data/24_light_df.csv')
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
        toVis.to_csv('saved_data/24_light_df_all_dates.csv', index=False)

        plot_count_day(alldays, toVis['title'])
        print('https://www.24tv.ua WAS PARSED')
    return 0


parse_24('нато')
