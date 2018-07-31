# -*- coding: utf-8 -*-

# 뉴스를 다시 긁어와 model을 통해 주제를 분석하여 링크와 이미지를 해당 주제에 저장하는 코드

from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
from datetime import timedelta, date
def daterange(date1, date2):
    for n in range(int((date2-date1).days)+1):
        yield date1 + timedelta(n)
import csv

from gensim import corpora, models
import gensim

from konlpy.tag import Hannanum
hannanum=Hannanum()

daum_url='http://media.daum.net/breakingnews/'
daum_url2='?regDate='
categoryList=['sports']
dateList=[]
start_dt = date(2018, 1, 1)
end_dt = date(2018, 7, 27)
for dt in daterange(start_dt, end_dt):
    dateList.append(dt.strftime("%Y%m%d"))
ntopic=100

save=[]
for i in range(0,100):
    save.append([])

for category in categoryList:
    ddlist=[]
    print(category,"start.....")
    for date in dateList:
        web_url=daum_url+category+daum_url2+date
        print("\t",web_url,"crawling links....")
        with urllib.request.urlopen(web_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            all_divs=soup.find_all("strong", {"class": "tit_thumb"})
            temp=list(map(lambda x:[x.a.text,x.a['href']],all_divs))
            title_list=[]
            url_list=[]
            for x in temp:
                if(x[0] in title_list):
                    continue
                title_list.append(x[0])
                url_list.append(x[1])
            print("\t\tcrawl each link...")
            #newpaper3k 통해서 일단 대충 파싱
            for url in url_list:
                a=Article(url, language='ko')
                a.download()
                a.parse()
                one=[url,a.top_image.split('fname=')[-1]]

                p=re.compile('\(.*?\)')
                word_list=[re.sub(p,"",x) for x in hannanum.nouns(a.text)]
                word_list=[re.sub('[^가-힝0-9a-zA-Z\\s]', '', x) for x in word_list]
                word_list=[x for x in word_list if len(x)>=2]

                LDA_MODEL=gensim.models.ldamodel.LdaModel.load('./model/'+category+'-'+str(ntopic)+'.model')
                doc=LDA_MODEL.id2word.doc2bow(word_list)
                topics_prob=sorted(LDA_MODEL.get_document_topics(doc),key=lambda x:x[1], reverse=True)
                topic=LDA_MODEL.show_topic(topics_prob[0][0],topn=30)
                save[topics_prob[0][0]].append(one)
                #print(word_list)
csvfile='./data/news_index/'+category+'-'+str(ntopic)+'.csv'
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(save)