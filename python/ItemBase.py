# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:47:24 2015

@author: Administrator
"""

import math
from operator import itemgetter
from Preprocess import exeTime

class ItemBase():
    
    def __init__(self, train):
        self.train = train
    
    @exeTime
    def ItemSimilarity(self):
        train = self.train
        #calculate co-rated users between items
        C = dict()
        N = dict()
        for users, items in train.items():
            for i in items.keys():
                if N.has_key(i):
                    N[i] += 1
                else:
                    N[i] = 1
                for j in items.keys():
                    if i == j:
                        continue
                    if C.has_key(i):
                        if C[i].has_key(j):
                            C[i][j] += 1
                        else:
                            C[i] = dict()
                            C[i][j] = 1
                    else:
                        C[i] = dict()
                        C[i][j] = 1
        #calculate finial similarity matrix W
        W = dict()
        for i,related_items in C.items():
            for j, cij in related_items.items():
                if W.has_key(i):
                    W[i][j] = cij / math.sqrt(N[i] * N[j])
                else:
                    W[i] = dict()
                    W[i][j] = cij / math.sqrt(N[i] * N[j])
        return(W)
    
    #ItemCF-IUF
    @exeTime
    def ItemSimilarity_adv(self):
        train = self.train
        #calculate co-rated users between items
        C = dict()
        N = dict()
        for users, items in train.items():
            for i in items.keys():
                if N.has_key(i):
                    N[i] += 1
                else:
                    N[i] = 1
                for j in items.keys():
                    if i == j:
                        continue
                    if C.has_key(i):
                        if C[i].has_key(j):
                            C[i][j] += 1 / math.log(1 + len(items) * 1.0)
                        else:
                            C[i] = dict()
                            C[i][j] = 1 / math.log(1 + len(items) * 1.0)
                    else:
                        C[i] = dict()
                        C[i][j] = 1 / math.log(1 + len(items) * 1.0)
        #calculate finial similarity matrix W
        W = dict()
        for i,related_items in C.items():
            for j, cij in related_items.items():
                if W.has_key(i):
                    W[i][j] = cij / math.sqrt(N[i] * N[j])
                else:
                    W[i] = dict()
                    W[i][j] = cij / math.sqrt(N[i] * N[j])
        return(W)
        
    def setMethod(self, method = 'normal'):
        if method == 'normal':
            self.W = self.ItemSimilarity()
        elif method == 'adv':
            self.W = self.ItemSimilarity_adv()
        return(self)
   
    #Item-CF
    @exeTime
    def Recommendation(self, user, K):
        W = self.W
        train = self.train
        rank = dict()
        ru = train[user]
        for i,pi in ru.items():
            for j, wj in sorted(W[i].items(), key = itemgetter(1), reverse=True)[0:K]:
                if j in ru:
                    continue
                if rank.has_key(j):
                    rank[j]['weight'] += float(pi) * float(wj)
                    rank[j]['reason'][i] = float(pi) * float(wj)
                else:
                    rank[j] = dict()
                    rank[j]['weight'] = dict()
                    rank[j]['reason'] = dict()
                    rank[j]['weight'] = float(pi) * float(wj)
                    rank[j]['reason'][i] = float(pi) * float(wj)
        rank = sorted(rank.items(), key=lambda e: e[1]['weight'],reverse = True)
        return(rank)   

if __name__ == '__main__':
    Reco = ItemBase(train)
    Reco = Reco.setMethod()
    rank = Reco.Recommendation('5989',10)