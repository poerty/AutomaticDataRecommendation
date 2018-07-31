import csv
import ast

categoryList=['sports']

for category in categoryList:
    with open('./data/news_index/'+category+'-100.csv', newline='') as file:
        reader = csv.reader(file)
        ddlist = list(map(tuple, reader))
        newlist=[]
        for idx,strlist in enumerate(ddlist):
            temp=[]
            for item in strlist:
                temp.append(ast.literal_eval(item))
            newlist.append(temp)

print(ddlist)

print(newlist)