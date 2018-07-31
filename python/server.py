# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler

import urllib

from io import BytesIO

from newspaper import Article

import csv
import re
import ast
import json

from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

from konlpy.tag import Hannanum
hannanum=Hannanum()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 
        self.end_headers()

        body=urllib.parse.parse_qs(self.path[2:])
        document=body['str'][0]
        print(document)

        p=re.compile('\(.*?\)')
        word_list=[re.sub(p,"",x) for x in hannanum.nouns(document)]
        word_list=[re.sub('[^가-힝0-9a-zA-Z\\s]', '', x) for x in word_list]
        word_list=[x for x in word_list if len(x)>=2]

        print(word_list)

        LDA_MODEL=gensim.models.ldamodel.LdaModel.load('./model/sports-100.model')
        doc=LDA_MODEL.id2word.doc2bow(word_list)
        print(LDA_MODEL.get_document_topics(doc))
        topics_prob=sorted(LDA_MODEL.get_document_topics(doc),key=lambda x:x[1], reverse=True)
        print(topics_prob)
        if(len(topics_prob)==0):
            self.wfile.write('fail'.encode('euc-kr'))        
            return
        else:
            print("no fail")
        topic=LDA_MODEL.show_topic(topics_prob[0][0],topn=60)
        print(topic)

        topic_words=[]
        for topic_word in topic:
            if topic_word[0] in document:
                topic_words.append(topic_word[0])

        print(topic_words)
        response_list=[]

        newlist=[]
        with open('./data/news_index/sports-100.csv', newline='') as file:
            reader = csv.reader(file)
            ddlist = list(map(tuple, reader))
            for idx,strlist in enumerate(ddlist):
                temp=[]
                for item in strlist:
                    temp.append(ast.literal_eval(item))
                newlist.append(temp)
        news_index=newlist[topics_prob[0][0]]
        for news in news_index:
            url=news[0]
            a=Article(url, language='ko')
            a.download()
            a.parse()
            p=re.compile('\(.*?\)')
            word_list=[re.sub(p,"",x) for x in hannanum.nouns(a.text)]
            word_list=[re.sub('[^가-힝0-9a-zA-Z\\s]', '', x) for x in word_list]
            word_list=[x for x in word_list if len(x)>=2]
            #todo : set 단어 count 반영
            match=0
            for word in topic_words:
                match=match+len(re.findall(word,a.text))
            response_list.append([url,news[1],match])
        
        response_list=sorted(response_list,key=lambda x:x[2], reverse=True)[:10]
        
        print("response",json.dumps(response_list).encode())
        self.wfile.write(json.dumps(response_list).encode())
        return

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 
        self.end_headers()
        response = BytesIO()
        
        
        document=body[4:].decode('utf-8')

        p=re.compile('\(.*?\)')
        word_list=[re.sub(p,"",x) for x in hannanum.nouns(document)]
        word_list=[re.sub('[^가-힝0-9a-zA-Z\\s]', '', x) for x in word_list]
        word_list=[x for x in word_list if len(x)>=2]

        LDA_MODEL=gensim.models.ldamodel.LdaModel.load('./model/sports-100.model')
        doc=LDA_MODEL.id2word.doc2bow(word_list)
        topics_prob=sorted(LDA_MODEL.get_document_topics(doc),key=lambda x:x[1], reverse=True)
        topic=LDA_MODEL.show_topic(topics_prob[0][0],topn=30)
        #topic index : print(topics_prob[0][0])
        #print(topic)
        topic_words=[]
        for topic_word in topic:
            if topic_word[0] in document:
                topic_words.append(topic_word[0])

        response_list=[]

        newlist=[]
        with open('./data/news_index/sports-100.csv', newline='') as file:
            reader = csv.reader(file)
            ddlist = list(map(tuple, reader))
            for idx,strlist in enumerate(ddlist):
                temp=[]
                for item in strlist:
                    temp.append(ast.literal_eval(item))
                newlist.append(temp)
        news_index=newlist[topics_prob[0][0]]
        for news in news_index:
            url=news[0]
            a=Article(url, language='ko')
            a.download()
            a.parse()
            p=re.compile('\(.*?\)')
            word_list=[re.sub(p,"",x) for x in hannanum.nouns(a.text)]
            word_list=[re.sub('[^가-힝0-9a-zA-Z\\s]', '', x) for x in word_list]
            word_list=[x for x in word_list if len(x)>=2]
            if(len(set(word_list) & set(topic_words))):
                response_list.append([url,news[1]])

        response.write(json.dumps(response_list).encode())
        print("!!")

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()