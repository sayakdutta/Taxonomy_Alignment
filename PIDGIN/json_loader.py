import json
import spacy
import re
import nltk
import os
#nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
from nltk import Tree
from nltk.stem import PorterStemmer
en_nlp = spacy.load('en_core_web_sm')

ps = PorterStemmer()

out=open("D://interlingua.txt","a",encoding='utf8')
stop_words = set(stopwords.words('english')) 

"""
def get(node,data,par):
    par.append(node.text)
    if(node.text==data):
        return par
    
    d=len(par)
    for child in node.children:
        m=get(child,data,par)
        if(m==None):
            continue
        if(len(m)!=d):
            return par
    par.pop()


def to_nltk_tree(node):
    #print(node.text)
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
"""
    
directory=r"C://Users//sayakdibyo//Pictures//btp_21//AN"

for filename in os.listdir(directory):
    f=open(os.path.join(directory,filename))
    if(not filename.endswith("json")):
        continue
    data=json.load(f)
    for val,i in enumerate(data):
        
        entities=[]
        names=[]
        start=0
        end=0
        for n,elem in enumerate(i["entities"]):
            
            if(n==1):
                if(elem[0] in i["tokens"]):
                    end=i["tokens"].index(elem[0])
                elif((re.split('[_,;:\t ]', elem[0]))[0] in i["tokens"]):
                    end=i["tokens"].index((re.split('[_,;:\t ]', elem[0]))[0])
                else:
                    break
            elif(n==0):
                if(elem[0] in i["tokens"]):
                    start=i["tokens"].index(elem[0])
                elif((re.split('[_,;:\t ]', elem[0]))[0] in i["tokens"]):
                    start=i["tokens"].index((re.split('[_,;:\t ]', elem[0]))[0])
            entities.append((re.split('[-_,;:\t ]', elem[0]))[-1])
            names.append(elem[0])
        
        
            
        if(len(names)!=2 or start>=end):
            continue
        #t=(re.split('[-_,;:.\t ]', names[1]))[0]
        for j in range(end-1,-1,-1):
            if(i["pos"][j].startswith("VB")):
                break
        
        r=""
        if(i["tokens"][j] in stop_words or j==0):
            for n in range(j,start):
                r+=i["tokens"][n]
        else:
            r=ps.stem(i["tokens"][j])
            
        if(r==""):
            continue
        y=names[1]
        x=names[0]
        
        out.write(x+"\t"+r+"\t"+y+"\n")
        out.write(y+"\t"+r+"\t"+x+"\n")
        f.close()
out.close()
