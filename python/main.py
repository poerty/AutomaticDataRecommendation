# -*- coding: utf-8 -*-

from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re

from konlpy.tag import Hannanum
hannanum=Hannanum()

daum_url='http://media.daum.net/breakingnews/'
daum_url2='?regDate='
categoryList=['society','digital']
dateList=['20180704','20180710']

for category in categoryList:
    for date in dateList:
        web_url=daum_url+category+daum_url2+date
        print(web_url," crawling links...")
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
            
            #newpaper3k 통해서 일단 대충 파싱
            for url in url_list:
                a=Article(url, language='ko')
                a.download()
                a.parse()
                p=re.compile('\(.*?\)')
                word_list=[re.sub(p,"",x) for x in hannanum.nouns(a.text) if len(x)>=2]
                word_list=[x for x in word_list if not('(' in x) and not(')' in x) and not(']' in x) and not('[' in x) and not('>' in x) and not('<' in x) and not('@' in x)]
                print(word_list)
