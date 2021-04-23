# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 11:22:02 2021

@author: sayakdibyo
"""
import numpy as np
from scipy.special import softmax
from scipy.optimize import curve_fit
from scipy import spatial
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import math
import json
from json import JSONEncoder

#convert numpy array to json
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def similarity(a,b,embed):
    if(np.linalg.norm(embed[a])==0 or np.linalg.norm(embed[b])==0):
        return 0
    return np.dot(embed[a],embed[b])/(np.linalg.norm(embed[a])*np.linalg.norm(embed[b]))
    

def gaussian(n,mean,var):
    if(var==0):
        return 0
    return (math.exp((-1*(n-mean)**2)/(2*var)))/math.sqrt(2*math.pi*var)
    

f=open("C://Users//sayakdibyo//Pictures//btp_21//output_new.txt","r",encoding='utf-8')
g=open("C://Users//sayakdibyo//Pictures//btp_21//output_final.txt","r",encoding='utf-8')
out=open("C://Users//sayakdibyo//Pictures//btp_21//embeddings.txt","w",encoding='utf-8')
gb=open("C://Users//sayakdibyo//Pictures//btp_21//garbage.txt","w",encoding='utf-8')
Lines = f.readlines()
d={}
cnt=0
counter={}
embed={}
for line in Lines:
    v=line.split("\t")
    if(v[0].startswith("wikidata")):
        d[v[0].split(":")[1]+"_equiv"]=cnt #indexing each wikidata vector
       
        counter[v[0]]=0
        cnt+=1

for line in Lines:
    v=line.split("\t")
    if(v[0].startswith("wikidata")):
        embed[v[0]]=np.zeros(len(d))
        embed[v[0]][d[v[0].split(":")[1]+"_equiv"]]=1 #create one-hot encoding for wikidata relation
        
        
Lines=g.readlines()

gauss={}
index=[]
for line in Lines:
    v=line.split("\t")
    embed[v[0]]=np.zeros(len(d))
    
    
    #embed[v[0]].fill(-1e9)
    sum=0
    tot=0
    cnt=0
    for k in range(1,len(v)-1,2):
        if(float(v[k+1])==0):
            break
        
        sum+=1/float(v[k+1])
        tot+=1
    if(tot==0):
        continue
    
    mean=sum/tot
    #mean=1/float(v[2])
    sum=0
    tot=0
    
    for k in range(1,min(41,len(v)-1),2):
        if(float(v[k+1])==0):
            break
        sum+=(1/float(v[k+1])-mean)**2
        tot+=1
    var=sum/tot
    
    for k in range(1,len(v)-1,2):
        #if(float(v[k+1])<0.0001):
            #continue
        #if(float(v[2])==0):
            #break
        diff=mean-1/float(v[2])
        if(float(v[k+1])==0):
           continue
        embed[v[0]][d[v[k]]]=gaussian(1/float(v[k+1])+diff,mean,var)

    #print(embed[v[0]])
        

    
    
    
for a in embed:
        l=[]
        if(a.startswith("dbpedia")):
            continue
        for b in embed:
            
            if(a!=b):
                l.append((similarity(a,b,embed),b))
       
        l.sort(reverse=True)
        if(l[0][0]>0):
            out.write(a+"\t"+str(l[0:10])+"\n")
        else:
            gb.write(a+"\t"+str(l[0:10])+"\n")


with open("data.json",'w') as f:
    json.dump(embed,f,cls=NumpyArrayEncoder)

f.close()
out.close()  
gb.close()
g.close()