# -*- coding: utf-8 -*-

# 뉴스를 긁어와 저장하는 코드

import csv
from konlpy.tag import Hannanum
from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
from datetime import timedelta, date

hannanum = Hannanum()


def getDaumUrl(category, date):
    return f'https://news.daum.net/breakingnews/{category}?regDate={date}'


def getCsvFilename(category):
    return f'./data/{category}.csv'


def daterange(date1, date2):
    for n in range(int((date2-date1).days)+1):
        yield date1 + timedelta(n)


def getDateList(start_date, end_date):
    date_list = []
    for dt in daterange(start_date, end_date):
        date_list.append(dt.strftime("%Y%m%d"))
    return date_list


def getNewsUrlListFromWebUrl(web_url):
    with urllib.request.urlopen(web_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        all_divs = soup.find_all("strong", {"class": "tit_thumb"})
        temp = list(map(lambda x: [x.a.text, x.a['href']], all_divs))
        title_list = []
        news_url_list = []
        for x in temp:
            if(x[0] in title_list):
                continue
            title_list.append(x[0])
            news_url_list.append(x[1])
        return news_url_list


def parseWordList(text):
    p = re.compile('\(.*?\)')
    word_list = [re.sub(p, "", x) for x in hannanum.nouns(text)]
    word_list = [re.sub('[^가-힝0-9a-zA-Z\\s]', '', x)
                 for x in word_list]
    word_list = [x for x in word_list if len(x) >= 2]
    return word_list


def parseNews(news_url):
    a = Article(news_url, language='ko')
    a.download()
    a.parse()
    info_url_list = [news_url, a.top_image.split('fname=')[-1]]

    return [a.text, info_url_list]


category_list = ['sports']
date_list = getDateList(date(2022, 1, 1), date(2022, 4, 20))

for category in category_list:
    ddlist = []
    print(category, "start.....")
    for date in date_list:
        web_url = getDaumUrl(category, date)
        print(f'\tStart crawl [{web_url}]')
        news_url_list = getNewsUrlListFromWebUrl(web_url)

        for news_url in news_url_list:
            [text, info_url_list] = parseNews(news_url)
            word_list = parseWordList(text)
            ddlist.append(word_list)

    csvfile = getCsvFilename(category)
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(ddlist)
