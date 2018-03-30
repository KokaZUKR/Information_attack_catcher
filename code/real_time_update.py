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

for i in range(n_iterations):
    page = requests.get('https://www.pravda.com.ua/news/')
    tree = html.fromstring(page.content)
    titles_parsed = tree.xpath('//div[@class="block block_news_all"]//div[@class="article__title"]/a/text()')
    print('===========================================================================================================')
    print('Parsed on {} sec:'.format(reload_sec * i))

    if i == 0:
        tit = titles_parsed
        print(tit)
    else:
        new_titles = new_news(titles_parsed, tit)
        if not new_titles:
            print('\nNo new titles found.')
        else:
            print('New titles:')
            print(new_titles)
            for new_title in new_titles:
                tit.insert(0, new_title)
        del new_titles[:]
        print('\nAll titles:')
        print(tit)
    print('===========================================================================================================')

    time.sleep(reload_sec)

print(tit)
