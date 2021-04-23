# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 11:33:43 2021

@author: sayakdibyo
"""


import re
import sys
import fileinput
import datetime
import operator
import os


f=open("C://Users//sayakdibyo//Pictures//btp_21//1.tsv","r",encoding='latin-1')
g=open("C://Users//sayakdibyo//Pictures//btp_21//_1.tsv","r",encoding='latin-1')
equiv=open("C://Users//sayakdibyo//Pictures//btp_21//paris_output.txt","r",encoding='utf-8')
sub=open("C://Users//sayakdibyo//Pictures//btp_21//subsump21_output.txt","r",encoding='utf-8')
#svo=open("E://interlingua.txt","r",encoding='utf-8')
out= open("C://Users//sayakdibyo//Pictures//btp_21//input_graph.txt", "w",encoding='utf-8')
seed=open("C://Users//sayakdibyo//Pictures//btp_21//seed.txt", "w",encoding="utf-8")
#db=open("C://Users//sayakdibyo//Pictures//btp_21//dbpedia_relations.txt","w",encoding='utf-8')
#wd=open("C://Users//sayakdibyo//Pictures//btp_21//wikidata_relations.txt","w",encoding='utf-8')
#db_count,wd_count={},{}



t1,t2=0,0
Lines = f.readlines() 	
rel=set()
for line in Lines: 
        t1+=1
        #if(t1>50000):
            #break
        #print(line)
        v=re.split('[-_,;:.\t ]', line)
		
		
        e1,e2="",""
        r=""
        #print(v)
        for i in range(len(v)):
            if(v[i]=="Person" or v[i]=="Location" or v[i]=="Organization"):
                r=v[i+1]
                break
        for j in range(i):
            e1+=v[j]
        for j in range(i+2,len(v)-1):
            e2+=v[j]
        e1=e1.lower()
        e2=e2.lower()
        r=r.lower()
        """
        if(r not in db_count):
            db_count[r]=1
        else:
            db_count[r]+=1
        """
        a="dbpedia:"+r
        b=e1+":"+e2
        out.write("%s\n" % "\t".join([a.rstrip("\n"), b.rstrip("\n"), "1.0"]))
        if r not in rel:
            rel.add(r)
            seed.write("%s\n" % "\t".join([a, r+"_equiv", "1.0"]))
            seed.write("%s\n" % "\t".join([a, r+"_sub", "1.0"]))
        
        
        
rel.clear()    
Lines = g.readlines() 	

for line in Lines: 
        t2+=1
        
        #if(t2>50000):
            #break
        #print(line)
        v=re.split('[-_,;:.\t ]', line)
		
		
        e1,e2="",""
        r=""
        #print(v)
        for i in range(len(v)):
            if(v[i]=="Person" or v[i]=="Location" or v[i]=="Organization"):
                r=v[i+1]
                break
        for j in range(i):
            e1+=v[j]
        for j in range(i+2,len(v)-1):
            e2+=v[j]
        e1=e1.lower()
        e2=e2.lower()
        r=r.lower()
        """
        if(r not in wd_count):
            wd_count[r]=1
        else:
            wd_count[r]+=1
        """
        a="wikidata:"+r
        b=e1+":"+e2
        out.write("%s\n" % "\t".join([a.rstrip("\n"), b.rstrip("\n"), "1.0"]))
        if r not in rel:
            rel.add(r)
            #seed.write("%s\n" % "\t".join([a, r+"_equiv", "1.0"]))
            #seed.write("%s\n" % "\t".join([a, r+"_sub", "1.0"]))
#print(sorted(db_count.items(), key=operator.itemgetter(1),reverse=True))  


cnt=0
for line in fileinput.input(files ='C://Users//sayakdibyo//Pictures//btp_21//interlingua.txt',openhook=fileinput.hook_encoded("utf-8")): 
                #if(cnt>2000000):
                    #break
                cnt+=1
                v=re.split('[\t]', line)
                e1,e2="",""
                r=""
                for i in v[0]:
                    if(i.isalnum()):
                        e1+=i
                        
                for i in v[1]:
                    if(i.isalnum()):
                        r+=i
                        
                for i in v[2]:
                    if(i.isalnum()):
                        e2+=i
        		
                e1=e1.lower()
                e2=e2.lower()
                r=r.lower()
                a="verb:"+r
                b=e1+":"+e2
                out.write("%s\n" % "\t".join([a.rstrip("\n"), b.rstrip("\n"), "1.0"]))
        
        
out.close()
print(cnt)
Lines=equiv.readlines()
for line in Lines:
    v=line.split()
    a="wikidata:"+v[1]
    b=v[0]+"_equiv"    
    seed.write("%s\n" % "\t".join([a.rstrip("\n"), b.rstrip("\n"), "1.0"]))
    
Lines=sub.readlines()
for line in Lines:
    v=line.split()
    a="wikidata:"+v[0]
    b=v[1]+"_sub"
        
    seed.write("%s\n" % "\t".join([a.rstrip("\n"), b.rstrip("\n"), "1.0"]))
    
seed.close()



#db.close()
#wd.close()

   
