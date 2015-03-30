# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:55:31 2015

@author: Administrator
"""

def Recommend(uid, familiarity, similarity, train):
    rank = dict()
    interacted_items = train[uid]
    for fid,fw in familiarity[uid]:
        for item,pw in train[fid]:
            # if user has already know the item
            # do not recommend it
            if item in interacted_items:
                continue
            addToDict(rank, item, fw * pw)
    for vid,sw in similarity[uid]:
        for item,pw in train[vid]:
            if item in interacted_items:
                continue
            addToDict(rank, item, sw * pw)
    return(rank)