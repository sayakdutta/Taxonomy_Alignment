# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:40:16 2021

@author: sayakdibyo
"""

import re
import sys
import fileinput
import datetime
import os

from wikidata.client import Client
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme




#out=open("C://Users//sayakdibyo//Pictures//btp_21//paris_output.txt","w");

"""
reld[r][x]:- dictionary that stores for each r and x in dbpedia,no of y for which r(x,y) exists
reldi[r][y]:-dictionary that stores for each r and y in dbpedia,no of x for which r^-1(y,x) exists
relw[r][x]:- dictionary that stores for each r and x in wikidata,no of y for which r(x,y) exists
relwi[r][y]:-dictionary that stores for each r and y in wikidata,no of x for which r^-1(y,x) exists
sub(i,j):- stores probability that i is subset of j
prob(i,j):-stores probability that i is equivalent to j with probability greater than 0.9
prob_y:- keeps track of y in dbpedia for which identical y' exists in wikidata
func_d and func_w:- functionality inverse of each relation in dbpedia and wikidata respectively
r1,r2:- set that stores first entity in dbpedia and wikidata respectively
all_entitypairs_d[r],all_entitypairs_w[r]:- set that stores all (x,y) pairs for each relation in dbpedia and wikidata respectively
rely_d[x]:- set that stores all (r,e2) pairs for dbpedia
relx_d[y]:- set that stores all (r,e1) pairs for dbpedia
rely_w[x]:- set that stores all (r,e2) pairs for wikidata
relx_w[y]:- set that stores all (r,e1) pairs for wikidata
"""
reld,relw,sub,prob,reldi,relwi={},{},{},{},{},{}
prob_y={}
func_d,func_w={},{}
all_entitypairs_d,all_entitypairs_w,rely_d,rely_w={},{},{},{}
relx_d,relx_w={},{}
r1,r2=set(),set()
en_db,en_wi=set(),set()
temp=set()

#Return 1 for lexicographically identical sentences
def probability(a,b):
    if(a==b):
        return 1.0
    else:
        return 0

#Traverse a directory and read tsv files
def read_file(path,s=''):
    if(s=="dbpedia"):
        t1=0
        for file in os.listdir(path):
            if(file.endswith("tsv")):
                
                f=open(os.path.join(path,file),"r",encoding='latin-1') #read dbpedia file
                Lines = f.readlines() 	
                for line in Lines: 
                        """
                        t1+=1
                        
                        if(t1>50000):
                            break
                        """
                        #print(line)
                        v=re.split('[-_,;:.\t ]', line)#split all names based on delimiters
                		
                		
                        e1,e2="",""
                        r=""
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
                        if r not in all_entitypairs_d.keys():
                            all_entitypairs_d[r]=set()
                        if e1 not in rely_d.keys():
                            rely_d[e1]=set()
                        if e2 not in relx_d.keys():
                            relx_d[e2]=set()
                        all_entitypairs_d[r].add((e1,e2))
                        #print(e1)
                        rely_d[e1].add((r,e2))
                        relx_d[e2].add((r,e1))
     
    else:
        t2=0
        for file in os.listdir(path):
            if(file.endswith("tsv")):
                
                g=open(os.path.join(path,file),"r",encoding='latin-1') #read wikidata file
                Lines = g.readlines() 	
            
                for line in Lines: 
                        
                        t2+=1
                        
                        if(t2>50000):
                            break
                        
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
                        if r not in all_entitypairs_w.keys():
                            all_entitypairs_w[r]=set()
                        if e1 not in rely_w.keys():
                            rely_w[e1]=set()
                        if e2 not in relx_w.keys():
                            relx_w[e2]=set()
                        all_entitypairs_w[r].add((e1,e2))
                        #print(e1)
                        rely_w[e1].add((r,e2))
                        relx_w[e2].add((r,e1))
                    

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
        if r not in all_entitypairs_w.keys():
            all_entitypairs_w[r]=set()
        if e1 not in rely_w.keys():
            rely_w[e1]=set()
        all_entitypairs_w[r].add((e1,e2));
        rely_w[e1].add((r,e2));
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
#Calculating inverse functionality of dbpedia/wikidata relations
def inv_functionality(a=''):
    if(a=="dbpedia"):
        for i in reldi.keys():
        		sum=0.0
        		for j in reldi[i].keys():
        			sum+=reldi[i][j]
                
        		func_d[i]=1.0/(sum/len(reldi[i]))
    else:
        for i in relwi.keys():
            sum=0.0
            for j in relwi[i].keys():
                sum+=relwi[i][j]
            
            func_w[i]=1.0/(sum/len(relwi[i]))


#Finding entity 2 in dbpedia that are also present in wikidata
def similar_y():
    for i in en_db:
        if i in en_wi:
            
            prob[(i,i)]=1
            if i in prob_y.keys():
                prob_y[i].add(i)
            else:
                prob_y[i]=set()
                prob_y[i].add(i)
                
                
def subset_calc(str=''):
	#Initialising subset probabilities=0.1
    if(str=="init"):
        for i in reld.keys():
            for j in relw.keys():
               
                sub[(i,j)]=0.1
                sub[(j,i)]=0.1
        return
    
    """Beginning subsumption calculation of each dbpedia rel wrt wikidata rel"""

    for m in reld.keys():
            sum2=0.0;
            
            """" Calculating denominator of subsumption calculation """
            for p in all_entitypairs_d[m]:
               	  
               	  prod2=1.0;
               	  for k in all_entitypairs_w:
   	   	
               	   	for l in all_entitypairs_w[k]:
   	   	
               	   		
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
            
            """" Calculating numerator of subsumption calculation """
            for n in relw.keys():
		
               sum1=0.0
               for p in all_entitypairs_d[m]:
               	  
                   prod1=1.0

                   for l in all_entitypairs_w[n]:
   	   	
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
               
               
		
        #print(datetime.datetime.now().time())

    """Beginning subsumption calculation of each wikidata rel wrt dbpedia rel"""
        
    for m in relw.keys():
            sum2=0.0;
            
            """ Calculating denominator of subsumption calculation """
            for p in all_entitypairs_w[m]:
               	  
               	  prod2=1.0;
               	  for k in all_entitypairs_d:
   	   	
               	   	for l in all_entitypairs_d[k]:
   	   	
               	   		
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
               
               
            """ Calculating numerator of subsumption calculation """   
            for n in reld.keys():
		
               sum1=0.0
               for p in all_entitypairs_w[m]:
               	  
                   prod1=1.0

                   for l in all_entitypairs_d[n]:
   	   	
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
    
#Calculates equivalence probabilities of each of the first entities of wikidata and dbpedia 
def equiv_calc():
    for itr in r1:
            
           
            #print(itr,len(temp))
            temp.clear()

            """ For each x in dbpedia,find y such that there exists a 
                y' in wikidata such that Pr(y==y')>=0.9 """
            for m in rely_d[itr]:
                if m[1] in prob_y.keys():
                    for n in prob_y[m[1]]:
                        #print(m[1],n)
                        for k in relx_w[n]:
                            temp.add(k[1])
                        
            """ Here we are calculating equivalence probabilities of plausible x and x' pairs """     
            for it in temp:
                prod=1.0
                #print(itr)
                for m in rely_d[itr]:
                    for n in rely_w[it]:
                        if (m[1],n[1]) not in prob.keys():
                            p=probability(m[1],n[1])
                        else:
                            p=prob[(m[1],n[1])]
                        
                        prod*=(1-sub[(n[0],m[0])]*func_d[m[0]]*p)*(1-sub[(m[0],n[0])]*func_w[n[0]]*p)
					
            
                if(prod<=0.1):
                    prob[(itr,it)]=prob[(it,itr)]=1-prod
                    if(itr in en_db and it in en_wi):
                        if itr in prob_y.keys():
                            prob_y[itr].add(it)
                        else:
                            prob_y[itr]=set()
                            prob_y[itr].add(it)
            
			        
"""
#Calculating inverse functionality of wikidata relations        
for i in relwi.keys():
		sum=0.0
		for j in relwi[i].keys():
			sum+=relwi[i][j]
        
		func_w[i]=1.0/(sum/len(relwi[i]))
"""
"""
iter=4
for i in reld.keys():
        for j in relw.keys():
               
            sub[(i,j)]=0.1;
            sub[(j,i)]=0.1;



"""
"""
temp=set()
for i in en_db:
    if i in en_wi:
        
        prob[(i,i)]=1
        if i in prob_y.keys():
            prob_y[i].add(i)
        else:
            prob_y[i]=set()
            prob_y[i].add(i)
"""

#This function performs the PARIS technique 
def paris_calc(iter=4):
    
    subset_calc("init")
    similar_y()
    inv_functionality("dbpedia")
    inv_functionality("wikidata")

    while(iter>0): #default no of iterations=4
        iter-=1
        equiv_calc()
        subset_calc()

"""        
while(iter>0):
        iter-=1
        print(datetime.datetime.now().time())
        for itr in r1:
            
           
            #print(itr,len(temp))
            temp.clear()
            for m in rely_d[itr]:
                if m[1] in prob_y.keys():
                    for n in prob_y[m[1]]:
                        #print(m[1],n)
                        for k in relx_w[n]:
                            temp.add(k[1])
                        
                
            for it in temp:
                prod=1.0
                #print(itr)
                for m in rely_d[itr]:
                    for n in rely_w[it]:
                        if (m[1],n[1]) not in prob.keys():
                            p=probability(m[1],n[1])
                        else:
                            p=prob[(m[1],n[1])]
                        prod*=(1-sub[(n[0],m[0])]*func[m[0]]*p)*(1-sub[(m[0],n[0])]*func_w[n[0]]*p)
					
            
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
            
            for p in all_entitypairs_d[m]:
               	  
               	  prod2=1.0;
               	  for k in all_entitypairs_w:
   	   	
               	   	for l in all_entitypairs_w[k]:
   	   	
               	   		
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
               for p in all_entitypairs_d[m]:
               	  
                   prod1=1.0

                   for l in all_entitypairs_w[n]:
   	   	
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
           
            for p in all_entitypairs_w[m]:
               	  
               	  prod2=1.0;
               	  for k in all_entitypairs_d:
   	   	
               	   	for l in all_entitypairs_d[k]:
   	   	
               	   		
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
               for p in all_entitypairs_w[m]:
               	  
                   prod1=1.0

                   for l in all_entitypairs_d[n]:
   	   	
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
	
		

		
               
"""
#print(len(reld),len(relw),len(prob))
if __name__=="__main__":
    
    
       
    read_file(sys.argv[1],"dbpedia")
    read_file(sys.argv[2],"wikidata")
    paris_calc()
    original_stdout = sys.stdout

    """ For each relation r in dbpedia,store a maximum equivalent unique relation r' in wikidata such that Pr(r==r')>=0.45"""
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

    """ For each relation r in dbpedia,store a all relations r' in wikidata such that Pr(r==r')>=0.45"""
    with open('C://Users//sayakdibyo//Pictures//btp_21//equiv_output.txt', 'w') as out:
        for itr in reld:
        
            for it in relw:
                sys.stdout=out
                #print(itr,it,sub[(itr,it)])
                if(sub[(itr,it)]*sub[(it,itr)]>=0.45):
                    print(itr,it)  
             
            sys.stdout=original_stdout
            
    original_stdout = sys.stdout

    """ Store subsumption probabilities of dbpedia wrt wikidata"""
    with open('C://Users//sayakdibyo//Pictures//btp_21//subsump12_output.txt', 'w') as out:
        for itr in reld:
        
            for it in relw:
                sys.stdout=out
                #print(itr,it,sub[(itr,it)])
                if(sub[(itr,it)]>=0.45):
                    print(itr,it)  
             
            sys.stdout=original_stdout
            
    original_stdout = sys.stdout

    """ Store subsumption probabilities of wikidata wrt dbpedia"""
    with open('C://Users//sayakdibyo//Pictures//btp_21//subsump21_output.txt', 'w') as out:
        for itr in reld:
        
            for it in relw:
                sys.stdout=out
                #print(itr,it,sub[(itr,it)])
                if(sub[(it,itr)]>=0.45):
                    print(it,itr)  
             
            sys.stdout=original_stdout


