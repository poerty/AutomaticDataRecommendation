# -*- coding: utf-8 -*-

# 뉴스를 다시 긁어와 model을 통해 주제를 분석하여 링크와 이미지를 해당 주제에 저장하는 코드

import csv
from konlpy.tag import Hannanum
import gensim
from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
from datetime import timedelta, date

hannanum = Hannanum()
ntopic = 100


def getDaumUrl(category, date):
    return f'http://media.daum.net/breakingnews/{category}?regDate={date}'


def getCsvFilename(category):
    return f'./data/news_index/{category}-{ntopic}.csv'


def getModelFilename(category):
    return f'./model/{category}-{ntopic}.model'


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


def getTopicList(category, word_list):
    topic_list_max_len = 5

    model_filename = getModelFilename(category)
    LDA_MODEL = gensim.models.ldamodel.LdaModel.load(model_filename)
    doc = LDA_MODEL.id2word.doc2bow(word_list)
    document_topics = LDA_MODEL.get_document_topics(doc)
    topic_list = sorted(document_topics, key=lambda x: x[1], reverse=True)
    return topic_list[0:topic_list_max_len]


def parseNews(news_url):
    a = Article(news_url, language='ko')
    a.download()
    a.parse()
    info_url_list = [news_url, a.top_image.split('fname=')[-1]]

    return [a.text, info_url_list]


category_list = ['sports']
date_list = getDateList(date(2018, 1, 1), date(2018, 7, 27))

save = []
for i in range(0, ntopic):
    save.append([])

for category in category_list:
    print(f'Start crawl [{category}]')
    for date in date_list:
        web_url = getDaumUrl(category, date)
        print(f'\tStart crawl [{web_url}]')
        news_url_list = getNewsUrlListFromWebUrl(web_url)

        for news_url in news_url_list:
            [text, info_url_list] = parseNews(news_url)
            word_list = parseWordList(text)
            topic_list = getTopicList(category, word_list)
            if len(topic_list) == 0 or len(word_list) == 0:
                continue
            save[topic_list[0][0]].append(info_url_list)

csvfile = getCsvFilename(category)
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(save)
