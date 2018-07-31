# -*- coding: utf-8 -*-

# model의 일관성을 측정하는 코드
import csv

import gensim
from gensim import corpora, models
from gensim.models import CoherenceModel

LDA_MODEL=gensim.models.ldamodel.LdaModel.load('./model/society.model')



categoryList=['society','politics','economic','foreign','culture','entertain','sports','digital','editorial']

ntopic=200
nword=30
for category in categoryList:

    ddlist=[]
    LDA_MODEL=gensim.models.ldamodel.LdaModel.load('./model/'+category+'.model')
    with open('./data/'+category+'.csv', newline='') as file:
        reader = csv.reader(file)
        ddlist = list(map(tuple, reader))
        dictionary=corpora.Dictionary(ddlist)
        corpus=[dictionary.doc2bow(doc) for doc in ddlist]

        topics=[]
        topic_list=LDA_MODEL.show_topics(num_topics=200,num_words=30,formatted=False)
        for idx,topic in topic_list:
            temp=[]
            for word in topic:
                temp.append(word[0])
            topics.append(temp)

        coherence_model_lda = CoherenceModel(topics=topics,corpus=corpus, dictionary=dictionary,coherence='u_mass')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)