import time
import warnings

import requests
from lxml import html

from code.usr_functions import new_news

warnings.filterwarnings("ignore")

tit_temp = []
tit = []
minutes_to_parse = 10  # how much time to spend parsing site
reload_sec = 5  # reload every ... seconds
n_iterations = int(minutes_to_parse * 60 / reload_sec)

for i in range(1, n_iterations):
    page = requests.get('https://www.pravda.com.ua/news/')
    tree = html.fromstring(page.content)
    titles_parsed = tree.xpath('//div[@class="block block_news_all"]//div[@class="article__title"]/a/text()')
    new_titles = new_news(titles_parsed, tit)
    print(new_titles)

    if not new_titles:
        print('-------------------')
        print('Parsed on {} sec'.format(i * reload_sec))
        print('NOTHING')
        print('-------------------')

    else:
        for i in range(len(new_titles) - 1, -1, -1):
            tit.append(new_titles[i])  # insert(0, new_titles[i])
        # tit = unlist_nested(tit)
        print('-------------------')
        print('Parsed on {} sec'.format(i * reload_sec))
        print(new_titles)
        print('-------------------')
        del new_titles[:]

    time.sleep(reload_sec)

print(tit)
