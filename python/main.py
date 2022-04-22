# -*- coding: utf-8 -*-
import csv

from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
p_stemmer = PorterStemmer()

categoryList = ['society', 'politics', 'economic', 'foreign',
                'culture', 'entertain', 'sports', 'digital', 'editorial']

ntopic = 100
nword = 30
for category in categoryList:
    ddlist = []
    with open('./data/'+category+'.csv', newline='') as file:
        reader = csv.reader(file)
        ddlist = list(map(tuple, reader))
        dictionary = corpora.Dictionary(ddlist)
        corpus = [dictionary.doc2bow(doc) for doc in ddlist]

        print("ntopic : ", ntopic, " start...")
        print("------------------------------------------------------")
        LDA_MODEL = gensim.models.ldamodel.LdaModel(
            corpus, num_topics=ntopic, id2word=dictionary, passes=50)
        # a=LDA_MODEL.show_topics(num_topics=ntopics,num_words=nwords)
        topic_list = LDA_MODEL.show_topics(
            num_topics=ntopic, num_words=nword, formatted=False)
        for idx, topic in topic_list:
            print(idx, " : ", end='')
            for word in topic:
                print(word[0], end=' ')
            print()
        print("------------------------------------------------------")
        print()
        LDA_MODEL.save('./model/'+category+'.model')
