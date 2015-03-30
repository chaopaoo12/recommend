# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 15:02:54 2015

@author: Administrator
"""

import random
import math
from operator import itemgetter
#item-pool 流行物品池
from Preprocess import exeTime

class LFM():
    
    def __init__(self, train):
        self.train = train
    
    @exeTime
    def item_popularity(self,num = 100):
        item_popularity = dict()
        for user, items in self.train.items():
            for item in items.keys():
                if item not in item_popularity:
                    item_popularity[item] = 0
                item_popularity[item] += 1
        self.items_pool = [key for key, value in item_popularity.items() if value >= num]
        return(self)
    
    def RandomSelectNegativeSample(self, items):
        ret = dict()
        for i in items.keys():
            ret[i] = 1
        n = 0
        for i in range(0, len(items) * 3):
            item = self.items_pool[random.randint(0, len(self.items_pool) - 1)]
            if item in ret:
                continue
            ret[item] = 0
            n += 1
            if n > len(items):
                break
        return(ret)
    
    @exeTime
    def InitModel(self, F):
        P = {i: dict(zip(range(0, F), [random.random()/math.sqrt(F) for x in range(0, F)])) for i in self.train.keys()}
        a = list(set([y for x in self.train.values() for y in x.keys()]))
        Q1 = {i: dict(zip(range(0, F), [random.random()/math.sqrt(F) for x in range(0, F)])) for i in a}
        Q = dict()
        for i in Q1.keys():
            for f in range(0,F):
                if Q.has_key(f):
                    Q[f][i] = Q1[i][f]
                else:
                    Q[f] = dict()
                    Q[f][i] = Q1[i][f]
        return(P, Q)
        
    def Predict(self, u, i):
        return(sum(self.P[u][f] * self.Q[f][i] for f in range(0,len(self.P[u]))))
    
    @exeTime
    def LatentFactorModel(self, F = 100, N = 10, alpha = 0.02, _lambda = 0.01):
        #user_items = self.train        
        self.P, self.Q = self.InitModel(F)
        for step in range(0, N):
            for user, items in self.train.items():
                samples = self.RandomSelectNegativeSample(items)
                for item, rui in samples.items():
                    eui = rui - self.Predict(user, item)
                    for f in range(0, F):
                        self.P[user][f] += alpha * (eui * self.Q[f][item] - _lambda * self.P[user][f])
                        self.Q[f][item] += alpha * (eui * self.P[user][f] - _lambda * self.Q[f][item])
            alpha *= 0.9
        return(self)
    
    @exeTime
    def Recommendation(self, user, N = 10):
        P, Q = self.P, self.Q
        rank = dict()
        item = self.train[user].keys()
        for f, puf in P[user].items():
            for i, qfi in Q[f].items():
                if i not in item:
                    if rank.has_key(i) == False:
                        rank[i] = puf * qfi
                    else:
                        rank[i] += puf * qfi
        rank = sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N-1]
        return(rank)