# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:46:21 2015

@author: Administrator

step one
calculate the matrix of user distance
step two
send 
"""

import math
from operator import itemgetter
from Preprocess import exeTime

class UserBase():
    
    def __init__(self, train):
        self.train = train
        
    #item-p
    @exeTime
    def UserSimilarity(self):
        train = self.train
        # build inverse table for item_users
        item_users = dict()
        for u, items in train.items():
            for i in items.keys():
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)
                
        #calculate co-rated items between users
        C = dict()
        N = dict()
        for i, users in item_users.items():
            for u in users:
                if N.has_key(u):
                    N[u] += 1
                else:
                    N[u] = 1
                for v in users:
                    if u == v:
                        continue
                    if C.has_key(u):
                        if C[u].has_key(v):
                            C[u][v] += 1
                        else:
                            C[u] = dict()
                            C[u][v] = 1
                    else:
                        C[u] = dict()
                        C[u][v] = 1
        #calculate finial similarity matrix W
        W = dict()
        for u, related_users in C.items():
            for v, cuv in related_users.items():
                if W.has_key(u):
                    W[u][v] = cuv / math.sqrt(N[u] * N[v])
                else:
                    W[u] = dict()
                    W[u][v] = cuv / math.sqrt(N[u] * N[v])                
        return(W)
        
    #User-IIF算法
    #惩罚用户共同兴趣列表中热门物品对他们相似度的影响
    @exeTime
    def UserSimilarity_adv(train):
        # build inverse table for item_users
        item_users = dict()
        for u, items in train.items():
            for i in items.keys():
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)
        #calculate co-rated items between users
        C = dict()
        N = dict()
        for i, users in item_users.items():
            for u in users:
                if N.has_key(u):
                    N[u] += 1
                else:
                    N[u] = 1
                for v in users:
                    if u == v:
                        continue
                    if C.has_key(u):
                        if C[u].has_key(v):
                            C[u][v] += 1 / math.log(1 + len(users))
                        else:
                            C[u] = dict()
                            C[u][v] = 1 / math.log(1 + len(users))
                    else:
                        C[u] = dict()
                        C[u][v] = 1 / math.log(1 + len(users))
        #calculate finial similarity matrix W
        W = dict()
        for u, related_users in C.items():
            for v, cuv in related_users.items():
                if W.has_key(u):
                    W[u][v] = cuv / math.sqrt(N[u] * N[v])
                else:
                    W[u] = dict()
                    W[u][v] = cuv / math.sqrt(N[u] * N[v])  
        return(W)
    
    def setMethod(self, method = 'normal'):
        if method == 'normal':
            self.W = self.UserSimilarity()
        elif method == 'adv':
            self.W = self.UserSimilarity_adv()
        return(self)
    

    #UserCF推荐算法
    @exeTime
    def Recommendation(self, user, K):
        W = self.W
        train = self.train
        rank = dict()
        interacted_items = train[user]
        for v, wuv in sorted(W[user].items(), key = itemgetter(1), reverse = True)[0 : K]:
            for i, rvi in train[v].items():
                if i in interacted_items:
                    #we should filter items user interacted before
                    continue
                if rank.has_key(i):
                    rank[i] += float(wuv) * float(rvi)
                else:
                    rank[i] = float(wuv) * float(rvi)
        rank = sorted(rank.items(), key=itemgetter(1), reverse = True)
        return(rank)
    



if __name__ == '__main__':
    UserReco = UserBase(train)
    UserReco = UserReco.setMethod()
    UserRank = UserReco.Recommendation('5989',10)