# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 10:13:42 2015

@author: Administrator
"""

def PersonalRank(G, user, alpha = 0.01):
    rank = dict()
    rank = {x:0 for x in G.keys()}
    rank[user] = 1
    for k in range(20):
        tmp = {x:0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                if j not in tmp:
                    tmp[j] = 0
                tmp[j] += 0.6 * rank[i] / (1.0 * len(ri))
                if j == user:
                    tmp[j] += 1 - alpha
        rank = tmp
    return(rank)
    
if __name__=='__main__':
    PerRank = PersonalRank(train,'5989') 