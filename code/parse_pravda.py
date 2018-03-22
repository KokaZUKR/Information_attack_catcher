import pandas as pd
import requests
from lxml import html

from code.usr_functions import *


def parse_pravda(keyword, save_big_csv=1, save_small_csv=1, save_all_and_plot=1):
    titles = []
    dates = []
    now, to = get_dates()
    curr_date = now

    #  REWRITE THIS LOOP INTO USR_FUNCTIONS!!!!
    #  REWRITE FROM LXML TO BEAUTIFUL SOUP!!!!!

    i = 1
    while curr_date > to:
        page = requests.get(
            'https://www.pravda.com.ua/search/page_' + str(i) + '/?search=' + str(cyrillic_url(keyword)))
        tree = html.fromstring(page.content)
        ptitles = tree.xpath('//div[@class="article__title"]/a/text()')[:30]
        pdates = tree.xpath('//div[@class="article article_search"]/div[@class="article__date"]/text()')[:30]
        pdates = [x[:10] for x in pdates]
        pdates = [datetime.datetime.strptime(date, '%d.%m.%Y').date() for date in pdates]
        titles.append(ptitles)
        dates.append(pdates)
        curr_date = pdates[29]
        i += 1

    dates = unlist_nested(dates)
    titles = unlist_nested(titles)

    dates = leave_list(dates, to)
    titles = titles[:len(dates)]

    fullDF = pd.DataFrame(
        {'title': titles,
         'date': dates,
         })

    if save_big_csv == 1:
        fullDF.to_csv('saved_data/pravda_big_df.csv', index=False)

    if save_small_csv == 1:
        lightDF = fullDF.groupby('date').count()
        lightDF.to_csv('saved_data/pravda_light_df.csv')

    if save_all_and_plot == 1:
        dftom = pd.read_csv('saved_data/pravda_light_df.csv')
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
        toVis.to_csv('saved_data/pravda_light_df_all_dates.csv', index=False)

        plot_count_day(alldays, toVis['title'])
        print('https://www.pravda.com.ua WAS PARSED')

    return 0
