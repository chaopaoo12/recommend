# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 08:56:46 2015

@author: Administrator
"""
import math

def RecentPopularity(records, alpha, T):
    ret = dict()
    for user,item,tm in records:
        if tm >= T:
            continue
        addToDict(ret, item, 1 / (1.0 + alpha * (T - tm)))
    return(ret)
    
def ItemSimilarity(train, alpha):
    #calculate co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i,tui in items.items():
            N[i] += 1
            for j,tuj in items.items():
                if i == j:
                    continue
                C[i][j] += 1 / (1 + alpha * abs(tui - tuj))
    #calculate finial similarity matrix W
    W = dict()
    for i,related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return(W)

#联系上下文的ItemCF
def Recommendation(train, user_id, W, K, t0):
    rank = dict()
    ru = train[user_id]
    for i,pi in ru.items():
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:
            if j, tuj in ru.items():
                continue
            rank[j] += pi * wj / (1 + alpha * (t0 - tuj))
    return(rank)


def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i,tui in items.items():
            if i not in item_users:
                item_users[i] = dict()
            item_users[i][u] = tui
    #calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u,tui in users.items():
            N[u] += 1
            for v,tvi in users.items():
                if u == v:
                    continue
                C[u][v] += 1 / (1 + alpha * abs(tui - tvi))
    #calculate finial similarity matrix W
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return(W)
    
def Recommendation(train, user_id, W, K, t0):
    rank = dict()
    ru = train[user_id]
    for i,pi in ru.items():
        for j, wj in sorted(W[i].items(), \
            key=itemgetter(1), reverse=True)[0:K]:
            if j,tuj in ru.items():
                continue
            rank[j] += pi * wj / (1 + alpha * (t0 - tuj))
    return rank

def Recommend(user, T, train, W):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(W[u].items, key=itemgetter(1),
        reverse=True)[0:K]:
        for i, tvi in train[v].items:
            if i in interacted_items:
            #we should filter items user interacted before
                continue
            rank[i] += wuv / (1 + alpha * (T - tvi))
    return(rank)
    
def PathFusion(user, time,G,alpha)
    Q = []
    V = set()
    depth = dict()
    rank = dict()
    depth['u:' + user] = 0
    depth['ut:' + user + '_' + time] = 0
    rank ['u:' + user] = alpha
    rank ['ut:' + user + '_' + time] = 1 - alpha
    Q.append('u:' + user)
    Q.append('ut:' + user + '_' + time)
    while len(Q) > 0:
        v = Q.pop()
        if v in V:
            continue
        if depth[v] > 3:
            continue
        for v2,w in G[v].items():
            if v2 not in V:
                depth[v2] = depth[v] + 1
                Q.append(v2)
            rank[v2] = rank[v] * w
    return(rank)