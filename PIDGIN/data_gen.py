# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 23:10:52 2021

@author: sayakdibyo
"""


import numpy as np
import operator

#fig = plt.figure(figsize=(12, 12))
#ax = plt.axes(projection='2d')

#np.set_printoptions(precision=5)


    

f=open("C://Users//sayakdibyo//Pictures//btp_21//outputall.txt","r",encoding='utf-8')
out=open("C://Users//sayakdibyo//Pictures//btp_21//outputall_final.txt","w",encoding='utf-8')
g=open("C://Users//sayakdibyo//Pictures//btp_21//outputall_new.txt","r",encoding='utf-8')
Lines = f.readlines()
db={}
dbi={}
cnt=0
for line in Lines:
    v=line.split("\t")
    if(v[0].startswith("dbpedia")):
        db[v[0].split(":")[1]+"_equiv"]=cnt
        dbi[cnt]=v[0].split(":")[1]+"_equiv"
        #if(v[0].split(":")[1]+"_equiv"=="educatedat_equiv"):
            #print(cnt)
        cnt+=1

Line = g.readlines()
wd={}
wdi={}
cnt=0
for line in Line:
    v=line.split("\t")
    if(v[0].startswith("wikidata")):
        wd[v[0].split(":")[1]+"_equiv"]=cnt
        wdi[cnt]=v[0].split(":")[1]+"_equiv"
        #if(v[0].split(":")[1]+"_equiv"=="educatedat_equiv"):
            #print(cnt)
        cnt+=1 

arr1=np.zeros(shape=(len(db),len(wd)))
arr2=np.zeros(shape=(len(db),len(wd)))
for line in Lines:
    v=line.split("\t")
    if(v[0].startswith("dbpedia")):
        continue
    
    #embed[v[0]].fill(-1e9)
   
    col=wd[v[0].split(":")[1]+"_equiv"]
    for k in range(1,len(v)-1,2):
        #if(float(v[k+1])<0.0001):
            #continue
        row=db[v[k]]
        val=float(v[k+1])
        arr1[row][col]=val
        
#print(np.dot(embed["wikidata:commanderof"], embed["wikidata:commander"])/(np.linalg.norm(embed["wikidata:commanderof"])*np.linalg.norm(embed["wikidata:commander"])))

for line in Line:
    v=line.split("\t")
    if(v[0].startswith("wikidata")):
        continue
    
    #embed[v[0]].fill(-1e9)
   
    row=db[v[0].split(":")[1]+"_equiv"]
    for k in range(1,len(v)-1,2):
        #if(float(v[k+1])<0.0001):
            #continue
        col=wd[v[k]]
        val=float(v[k+1])
        arr2[row][col]=val
        
arr1=np.multiply(arr1,arr2)

for x in range(0,arr1.shape[0]):
    d={}
    rel="dbpedia:"+dbi[x].split("_")[0]
    out.write(rel+"\t")
    for y in range(0,arr1.shape[1]):
        
        d[wdi[y]]=arr1[x][y]
    
    for key in sorted(d.items(), key=operator.itemgetter(1),reverse=True):
        out.write(key[0]+"\t")
        out.write(str(key[1])+"\t")
    out.write("\n")
    
f.close()
g.close()
out.close()
        
            
 