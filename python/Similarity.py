# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:45:34 2015

@author: Administrator
"""

import math

#余弦相似度
def UserSimilarity_th(train):
    W = dict()
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue
            W[u][v] = len(train[u] & train[v])
            W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
    return W
 
#item-p    
def UserSimilarity(train):
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
    
#物品相似度
def ItemSimilarity(train):
    #calculate co-rated users between items
    C = dict()
    N = dict()
    for users, items in train.items():
        for i in users:
            if N.has_key(i):
                N[i] += 1
            else:
                N[i] = 1
            for j in users:
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
    return W
    
#ItemCF-IUF
def ItemSimilarity_adv(train):
    #calculate co-rated users between items
    C = dict()
    N = dict()
    for users, items in train.items():
        for i in users:
            if N.has_key(i):
                N[i] += 1
            else:
                N[i] = 1
            for j in users:
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
    return W