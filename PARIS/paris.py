# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:40:16 2021

@author: sayakdibyo
"""

import re
import sys
import fileinput
import datetime

from wikidata.client import Client
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme


f=open("C://Users//sayakdibyo//Pictures//btp_21//1.tsv","r",encoding='latin-1') #read dbpedia file
g=open("C://Users//sayakdibyo//Pictures//btp_21//_1.tsv","r",encoding='latin-1') #read wikidata file

#out=open("C://Users//sayakdibyo//Pictures//btp_21//paris_output.txt","w");

"""
reld[r][x]:- dictionary that stores for each r and x in dbpedia,no of y for which r(x,y) exists
reldi[r][y]:-dictionary that stores for each r and y in dbpedia,no of x for which r^-1(y,x) exists
sub(i,j):- stores probability that i is subset of j
prob(i,j):-stores probability that i is equivalent to j with probability greater than 0.9
prob_y:- keeps track of y in dbpedia for which identical y' exists in wikidata
func and funcl:- functionality inverse of each relation in dbpedia and wikidata respectively
r1,r2:- set that stores first entity in dbpedia and wikidata respectively
cnt1[r],cnt2[r]:- set that stores all (x,y) pairs for each relation in dbpedia and wikidata respectively
chk1[x]:- set that stores all (r,e2) pairs for dbpedia
chk1_r[y]:- set that stores all (r,e2) pairs for dbpedia
"""
reld,relw,sub,prob,reldi,relwi={},{},{},{},{},{}
prob_y={}
func,funcl={},{}
cnt1,cnt2,chk1,chk2={},{},{},{}
chk1_r,chk2_r={},{}
r1,r2=set(),set()
en_db,en_wi=set(),set()

#Return 1 for lexicographically identical sentences
def probability(a,b):
    if(a==b):
        #prob[(a,b)]=1.0
        return 1.0
    else:
        #prob[(a,b)]=1e-6
        #prob[(b,a)]=1e-6
        return 0

t1,t2=0,0
Lines = f.readlines() 	
for line in Lines: 
        """
        t1+=1
        
        if(t1>50000):
            break
        """
        #print(line)
        v=re.split('[-_,;:.\t ]', line)
		
		
        e1,e2="",""
        r=""
        #print(v)
        for i in range(len(v)):  #find the position of relation
            if(v[i]=="Person" or v[i]=="Location" or v[i]=="Organization"):
                r=v[i+1]
                break
        for j in range(i): #get first entity
            e1+=v[j]
        for j in range(i+2,len(v)-1):  #get second entity
            e2+=v[j]
        e1=e1.lower()+"_"+v[i].lower()   
        e2=e2.lower()+"_"+(v[-1].rstrip()).lower()
        r=r.lower()
        
        #e1=e1+"_"+r
        #e2=e2+"_"+v[-1].lower()
        if r not in reld.keys():
            reld[r]={}
            reldi[r]={}
        if e1 not in reld[r].keys():
            reld[r][e1]=1.0
        else:
            reld[r][e1]+=1
        if e2 not in reldi[r].keys():
            reldi[r][e2]=1.0
        else:
            reldi[r][e2]+=1
        r1.add(e1)
        #en_db.add(e1)
        en_db.add(e2)
        if r not in cnt1.keys():
            cnt1[r]=set()
        if e1 not in chk1.keys():
            chk1[e1]=set()
        if e2 not in chk1_r.keys():
            chk1_r[e2]=set()
        cnt1[r].add((e1,e2))
        #print(e1)
        chk1[e1].add((r,e2))
        chk1_r[e2].add((r,e1))
        
Lines = g.readlines() 	

for line in Lines: 
        """
        t2+=1
        
        if(t2>50000):
            break
        """
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
        e1=e1.lower()+"_"+v[i].lower()
        e2=e2.lower()+"_"+(v[-1].rstrip()).lower()
        r=r.lower()
        
        #e1=e1+"_"+r
        #e2=e2+"_"+v[-1].lower()
        if r not in relw.keys():
            relw[r]={}
            relwi[r]={}
        if e1 not in relw[r].keys():
            relw[r][e1]=1.0
        else:
            relw[r][e1]+=1
        if e2 not in relwi[r].keys():
            relwi[r][e2]=1.0
        else:
            relwi[r][e2]+=1
        r2.add(e1)
        #en_wi.add(e1)
        en_wi.add(e2)
        if r not in cnt2.keys():
            cnt2[r]=set()
        if e1 not in chk2.keys():
            chk2[e1]=set()
        if e2 not in chk2_r.keys():
            chk2_r[e2]=set()
        cnt2[r].add((e1,e2))
        #print(e1)
        chk2[e1].add((r,e2))
        chk2_r[e2].add((r,e1))
        

"""
Lines = g.readlines() 

for line in Lines: 

        t2+=1
        if(t2>100000):
            break
        
        

        v=re.split('[-_,;:\t ]', line)
        q42_dict = get_entity_dict_from_api(v[0])
        q42 = WikidataItem(q42_dict)
        e1 = q42.get_label()
        
        q42_dict = get_entity_dict_from_api(v[1])
        q42 = WikidataProperty(q42_dict)
        r = q42.get_label()
        
       
        q42_dict = get_entity_dict_from_api(v[2][:-1])
        q42 = WikidataItem(q42_dict)
        e2 = q42.get_label()
        
        
        v=re.split('[-_,;:\t ]', e1)
        e1=""
        for i in v:
            e1+=i
        v=re.split('[-_,;:\t ]', r)
        r=""
        for i in v:
            r+=i
        v=re.split('[-_,;:\t ]', e2)
        e2=""
        for i in v:
            e2+=i
        e1=e1.lower()
        e2=e2.lower()
        r=r.lower()
        #print(e1,r,e2)
        if r not in relw.keys():
            relw[r]={}
            relwi[r]={}
        if e1 not in relw[r].keys():
            relw[r][e1]=1.0
        else:
            relw[r][e1]+=1
        if e2 not in relwi[r].keys():
            relwi[r][e2]=1.0
        else:
            relwi[r][e2]+=1
        r2.add(e1);
        en_wi.add(e1)
        en_wi.add(e2);
        if r not in cnt2.keys():
            cnt2[r]=set()
        if e1 not in chk2.keys():
            chk2[e1]=set()
        cnt2[r].add((e1,e2));
        chk2[e1].add((r,e2));
"""


        
"""    
original_stdout = sys.stdout
with open('C://Users//sayakdibyo//Pictures//btp_21//old_instance.txt', 'w') as out:
    for it in en_db:
            sys.stdout=out
            print(it,it,1)
            
            for itr in en_wi:
                if(it!=itr):
                    print(it,itr,1e-6)
                    print(itr,it,1e-6)
    		  	
                   
            sys.stdout=original_stdout
            
    for it in en_wi:
        if it not in en_db:
            sys.stdout=out
            print(it,it,1)
            sys.stdout=original_stdout
 
out.close()
"""
#Calculating inverse functionality of dbpedia relations
for i in reldi.keys():
		sum=0.0
		for j in reldi[i].keys():
			sum+=reldi[i][j]
        
		func[i]=1.0/(sum/len(reldi[i]))

#Calculating inverse functionality of wikidata relations        
for i in relwi.keys():
		sum=0.0
		for j in relwi[i].keys():
			sum+=relwi[i][j]
        
		funcl[i]=1.0/(sum/len(relwi[i]))
	
iter=4
for i in reld.keys():
        for j in relw.keys():
               
            sub[(i,j)]=0.1;
            sub[(j,i)]=0.1;




temp=set()
for i in en_db:
    if i in en_wi:
        
        prob[(i,i)]=1
        if i in prob_y.keys():
            prob_y[i].add(i)
        else:
            prob_y[i]=set()
            prob_y[i].add(i)


while(iter>0):
        iter-=1
        print(datetime.datetime.now().time())
        for itr in r1:
            
           
            #print(itr,len(temp))
            temp.clear()
            for m in chk1[itr]:
                if m[1] in prob_y.keys():
                    for n in prob_y[m[1]]:
                        #print(m[1],n)
                        for k in chk2_r[n]:
                            temp.add(k[1])
                        
                
            for it in temp:
                prod=1.0
                #print(itr)
                for m in chk1[itr]:
                    for n in chk2[it]:
                        if (m[1],n[1]) not in prob.keys():
                            p=probability(m[1],n[1])
                        else:
                            p=prob[(m[1],n[1])]
                        prod*=(1-sub[(n[0],m[0])]*func[m[0]]*p)*(1-sub[(m[0],n[0])]*funcl[n[0]]*p)
					
            
                if(prod<=0.1):
                    prob[(itr,it)]=prob[(it,itr)]=1-prod
                    if(itr in en_db and it in en_wi):
                        if itr in prob_y.keys():
                            prob_y[itr].add(it)
                        else:
                            prob_y[itr]=set()
                            prob_y[itr].add(it)
            
			
        print(datetime.datetime.now().time())
        print(len(reld))
        for m in reld.keys():
            sum2=0.0;
            
            for p in cnt1[m]:
               	  
               	  prod2=1.0;
               	  for k in cnt2:
   	   	
               	   	for l in cnt2[k]:
   	   	
               	   		
                                  if (p[0],l[0]) not in prob.keys():
                                     x=probability(p[0],l[0])
                                  else:
                                      x=prob[(p[0],l[0])]
                                          
                                
                                  if (p[1],l[1]) not in prob.keys():
                                     y=probability(p[1],l[1])
                                  else:
                                      y=prob[(p[1],l[1])]
                                  prod2=prod2*(1-x*y)
   	   	    
   	   	
   	   	
                           	   
                  sum2+=1-prod2;
            
            for n in relw.keys():
		
               sum1=0.0
               for p in cnt1[m]:
               	  
                   prod1=1.0

                   for l in cnt2[n]:
   	   	
                       if (p[0],l[0]) not in prob.keys():
                                     x=probability(p[0],l[0])
                       else:
                                      x=prob[(p[0],l[0])]
                                          
                                
                       if (p[1],l[1]) not in prob.keys():
                                     y=probability(p[1],l[1])
                       else:
                                      y=prob[(p[1],l[1])]
                       prod1=prod1*(1-x*y)
               	   	
               	   sum1+=1-prod1;
               
               if(sum2==0):
                   sub[(m,n)]=0
               else:
                   sub[(m,n)]=sum1/sum2;
               
               
		
        print(datetime.datetime.now().time())
        
        for m in relw.keys():
            sum2=0.0;
           
            for p in cnt2[m]:
               	  
               	  prod2=1.0;
               	  for k in cnt1:
   	   	
               	   	for l in cnt1[k]:
   	   	
               	   		
                          if (p[0],l[0]) not in prob.keys():
                                     x=probability(p[0],l[0])
                          else:
                                      x=prob[(p[0],l[0])]
                                          
                                
                          if (p[1],l[1]) not in prob.keys():
                                     y=probability(p[1],l[1])
                          else:
                                      y=prob[(p[1],l[1])]
                          prod2=prod2*(1-x*y)
   	   	    
   	   	
   	   	
                           	   
               	  sum2+=1-prod2
               
               
               
            for n in reld.keys():
		
               sum1=0.0
               for p in cnt2[m]:
               	  
                   prod1=1.0

                   for l in cnt1[n]:
   	   	
                           if (p[0],l[0]) not in prob.keys():
                                     x=probability(p[0],l[0])
                           else:
                                      x=prob[(p[0],l[0])]
                                          
                                
                           if (p[1],l[1]) not in prob.keys():
                                     y=probability(p[1],l[1])
                           else:
                                      y=prob[(p[1],l[1])]
                           prod1=prod1*(1-x*y)
               	   	
               	   sum1+=1-prod1;
               if(sum2==0):
                   sub[(m,n)]=0
               else:
                   sub[(m,n)]=sum1/sum2;
	
		

		
               

#print(len(reld),len(relw),len(prob))
original_stdout = sys.stdout
with open('C://Users//sayakdibyo//Pictures//btp_21//paris_output.txt', 'w') as out:
    for itr in reld:
        maxi=0.0
        for it in relw:
            sys.stdout=out
            #print(itr,it,sub[(itr,it)])
            if(sub[(itr,it)]*sub[(it,itr)]>maxi):
                maxi=sub[(itr,it)]*sub[(it,itr)]
                y=it
        if(maxi>=0.45):
            print(itr,y,maxi)   
        sys.stdout=original_stdout
    
original_stdout = sys.stdout
with open('C://Users//sayakdibyo//Pictures//btp_21//equiv_output.txt', 'w') as out:
    for itr in reld:
    
        for it in relw:
            sys.stdout=out
            #print(itr,it,sub[(itr,it)])
            if(sub[(itr,it)]*sub[(it,itr)]>=0.45):
                print(itr,it)  
         
        sys.stdout=original_stdout
        
original_stdout = sys.stdout
with open('C://Users//sayakdibyo//Pictures//btp_21//subsump12_output.txt', 'w') as out:
    for itr in reld:
    
        for it in relw:
            sys.stdout=out
            #print(itr,it,sub[(itr,it)])
            if(sub[(itr,it)]>=0.45):
                print(itr,it)  
         
        sys.stdout=original_stdout
        
original_stdout = sys.stdout
with open('C://Users//sayakdibyo//Pictures//btp_21//subsump21_output.txt', 'w') as out:
    for itr in reld:
    
        for it in relw:
            sys.stdout=out
            #print(itr,it,sub[(itr,it)])
            if(sub[(it,itr)]>=0.45):
                print(it,itr)  
         
        sys.stdout=original_stdout


