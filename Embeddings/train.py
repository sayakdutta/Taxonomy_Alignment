# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:43:01 2021

@author: sayakdibyo
"""

import torch
import torch.nn as nn
import json
import math
import numpy as np
import sys

f=open("C://Users//sayakdibyo//Pictures//btp_21//output.txt","r",encoding='utf-8')
out=open("C://Users//sayakdibyo//Pictures//btp_21//embeddings_train.txt","w",encoding='utf-8')
Lines=f.readlines()
d={}
cnt=0
torch.set_printoptions(precision=20)
#print(torch.cuda.get_device_name(0))
for line in Lines:
    v=line.split("\t")
    if(v[0].startswith("dbpedia")):
        d[v[0]]=cnt
        cnt+=1

def similarity(a,b,embed):
    if(np.linalg.norm(torch.flatten(embed[a]))==0 or np.linalg.norm(torch.flatten(embed[b]))==0):
        return 0
    return np.dot(torch.flatten(embed[a]),torch.flatten(embed[b]))/(np.linalg.norm(torch.flatten(embed[a]))*np.linalg.norm(torch.flatten(embed[b])))

class Neural_Network(nn.Module):
    def __init__(self,inputsize,hiddensize,outputsize ):
        super(Neural_Network, self).__init__()
        # parameters
       
        self.inputSize = inputsize
        self.outputSize = outputsize
        self.hiddenSize = hiddensize
        
        # weights
        self.W1 = torch.randn(self.inputSize, self.hiddenSize,dtype=torch.double) # 2 X 3 tensor
        self.W2 = torch.randn(self.hiddenSize, self.outputSize,dtype=torch.double) # 3 X 1 tensor
        #print(self.W1,self.W2)
    
    
    def forward(self, X):
        
        self.z = torch.matmul(X, self.W1) #input to hidden layer multiplication
        #print(self.z)
        self.z2 = self.sigmoid(self.z) # activation function
        
        self.z3 = torch.matmul(self.z2, self.W2)
        
        o = self.sigmoid(self.z3) # final activation function
        """
        if(torch.isnan(o).any()):
            print(o,"gotcha")
            sys.exit()
        """
        return o
    
    def calc(self,X):
        self.z = torch.matmul(X, self.W1) 
        #print(self.z)
        self.z2 = self.sigmoid(self.z)
        #self.z3 = torch.matmul(self.z2, self.W2)
        
        #o = self.sigmoid(self.z3) # final activation function
        return self.z2
        
    def sigmoid(self, s):
        return torch.sigmoid(s.to(dtype=torch.float64))
        #return 1 / (1 + torch.exp(-s).to(dtype=torch.float64))
    
    def sigmoidPrime(self, s):
        # derivative of sigmoid
        return s * (1 - s)
    
    def ce_loss(self,x,y):
        sum=0
        for i in range(len(x)):
            #print(x[i])
            sum-=(y[i]*math.log(x[i]+1e-15)+(1-y[i])*math.log(1+1e-15-x[i]))
        return sum
        
    def backward(self, X, y, o):
        #self.o_error = y - o # error in output
        self.o_error=torch.div(y,1e-15+o)-torch.div(1-y,1+1e-15-o)
        
        for i in range(len(y[0])):
            if(y[0][i]==0):
                self.o_error[0][i]=0
        
        self.o_delta = self.o_error * self.sigmoidPrime(o) # derivative of sig to error
        
        self.z2_error = torch.matmul(self.o_delta, torch.t(self.W2))
        
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)
        #print(torch.t(self.z2_error).size(), self.o_delta.size())
        #print(o,1-o)
        self.W2 += 0.01*torch.matmul(torch.t(self.z2_error), self.o_delta)
        self.W1 += 0.01*torch.matmul(torch.t(X), self.z2_delta)
        
        #return torch.dist(torch.flatten(y),torch.flatten(o),2)**2
        
        return self.ce_loss(torch.flatten(o),torch.flatten(y))
        
    def train(self, X, y):
        # forward + backward pass for training
        sum=0.0
        #cnt=0
        for i in X:
            o = self.forward(torch.DoubleTensor(X[i]).view(1,len(X[i])))
            sum+=self.backward(torch.DoubleTensor(X[i]).view(1,len(X[i])), torch.DoubleTensor(y[i]).view(1,len(y[i])), o)
            #print(sum)
            
        #return math.sqrt(sum/len(X))
        return sum/len(X)
        
    def saveWeights(self, model):
        # we will use the PyTorch internal storage functions
        torch.save(model, "NN")
        # you can reload model with all the weights and so forth with:
        # torch.load("NN")
    
    def predict(self,test_x):
        test={}
        for i in test_x:
            test[i]=self.calc(torch.DoubleTensor(test_x[i]).view(1,len(test_x[i])))
        return test
     
f = open('C://Users//sayakdibyo//Pictures//btp_21//data.json',)
data = json.load(f) 
train_x={}
test_x={}
truth={}
for i in data:
    if(i.startswith("dbpedia")):
        train_x[i]=data[i]
        truth[i]=[0]*len(d)
        truth[i][d[i]]=1
    test_x[i]=data[i]

#print(type(train_x[i]))
inputsize=len(train_x[i])
outputsize=len(d)    
NN = Neural_Network(inputsize,100,outputsize)
#NN=torch.load("NN")
NN.to(torch.device("cuda:0"))


for i in range(100):  # trains the for 100 epochs
    loss=NN.train(train_x, truth)
    print("Loss after "+str(i+1)+" Epoch is:"+str(loss))
    #if(loss<mini):
    NN.saveWeights(NN)
    #mini=loss  

"""
test=NN.predict(test_x)
for a in test:
    l=[]
    if(a.startswith("dbpedia")):
        continue
    for b in test:
        if(a!=b ):
            #print(test[b],test_x[b])
            l.append((similarity(a,b,test),b))
            
    l.sort(reverse=True)
    out.write(a+"\t"+str(l[0:10])+"\n")
    
   
out.close()
"""