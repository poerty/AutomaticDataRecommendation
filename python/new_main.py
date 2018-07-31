# -*- coding: utf-8 -*-
import csv

from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from gensim.models import CoherenceModel
import gensim
p_stemmer=PorterStemmer()
#'society','politics','economic','foreign','culture','entertain',
categoryList=['sports']
#,'digital','editorial'

ntopics=[10,15,20,30,40,50,60,70,80,90,100,150,200]
nword=30
for ntopic in ntopics:
    print("ntopic : ",ntopic," start...")
    print("------------------------------------------------------")
    for category in categoryList:
        ddlist=[]
        with open('./data/'+category+'.csv', newline='') as file:
            reader = csv.reader(file)
            ddlist = list(map(tuple, reader))
            dictionary=corpora.Dictionary(ddlist)
            corpus=[dictionary.doc2bow(doc) for doc in ddlist]

            
            LDA_MODEL=gensim.models.ldamodel.LdaModel(corpus,num_topics=ntopic,id2word=dictionary, passes=50)
            #a=LDA_MODEL.show_topics(num_topics=ntopics,num_words=nwords)
            topics=[]
            topic_list=LDA_MODEL.show_topics(num_topics=ntopic,num_words=nword,formatted=False)
            for idx,topic in topic_list:
                temp=[]
                for word in topic:
                    temp.append(word[0])
                topics.append(temp)

            coherence_model_lda = CoherenceModel(model=LDA_MODEL,texts=ddlist, dictionary=dictionary,coherence='c_v')
            coherence_lda = coherence_model_lda.get_coherence()
            print(category+' Coherence Score: ', coherence_lda)
            LDA_MODEL.save('./model/'+category+'-'+str(ntopic)+'.model')
    print("------------------------------------------------------")