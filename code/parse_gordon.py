import datetime

import pandas as pd
import requests
from lxml import html

from code.usr_functions import leave_list, get_dates, unlist_nested, plot_count_day, months24


def parse_gordon(keyword, save_big_csv=1, save_small_csv=1, save_all_and_plot=1):
    titles = []
    dates = []
    now, to = get_dates()
    curr_date = now

    j = 1
    while curr_date > to:

        page = requests.get('http://gordonua.com/ukr/search/p' + str(j) + '.html?s[text]=' + keyword + '&')
        tree = html.fromstring(page.content)
        title = tree.xpath('//div[@class="lenta_head"]/a/text()')
        date = tree.xpath('//div[@class="for_data"]/text()')
        date = [i[:-6].replace(',', '') for i in date]
        for i in range(len(date)):
            if date[i] == 'Сьогодні':
                date[i] = datetime.datetime.now().date()
            elif date[i] == 'Учора':
                date[i] = datetime.datetime.now().date() - datetime.timedelta(1)
            else:
                splt = date[i].split()
                splt[1] = months24[splt[1]]

                for k in range(len(splt)):
                    splt[k] = int(splt[k])
                date[i] = datetime.date(splt[2], splt[1], splt[0])
        curr_date = date[-1]
        titles.append(title)
        dates.append(date)
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
        fullDF.to_csv('saved_data/gordon_big_df.csv', index=False)

    if save_small_csv == 1:
        lightDF = fullDF.groupby('date').count()
        lightDF.to_csv('saved_data/gordon_light_df.csv')

    if save_all_and_plot == 1:
        dftom = pd.read_csv('saved_data/gordon_light_df.csv')
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
        toVis.to_csv('saved_data/gordon_light_df_all_dates.csv', index=False)

        plot_count_day(alldays, toVis['title'], name='GORDON')
        print('gordon WAS PARSED')

    return 0


