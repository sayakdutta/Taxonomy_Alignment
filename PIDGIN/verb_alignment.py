# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 19:22:17 2021

@author: sayakdibyo
"""

f=open("C://Users//sayakdibyo//Pictures//btp_21//phrases.txt","r",encoding='latin-1')
out=open("C://Users//sayakdibyo//Pictures//btp_21//phrase_alignments.txt","w",encoding='latin-1')
lines=f.readlines()
d={}
for line in lines:
    v=line.split("\t")
    if(v[1] not in d.keys()):
        d[v[1]]=[]
    d[v[1]].append(v[0])
    
for k in d:
    out.write(k+"\t")
    for i in range(len(d[k])):
        if(len(d[k][i][5:])<=20):
            out.write(d[k][i]+"\t") 
    out.write("\n")
out.close()
