# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 11:17:51 2015

@author: Administrator
"""
import math
import pandas as pd

def CosineSim(item_tags, i, j):
    ret = 0
    for b,wib in item_tags[i].items():
        if b in item_tags[j]:
            ret += wib * item_tags[j][b]
    ni = 0
    nj = 0
    for b, w in item_tags[i].items():
        ni += w * w
    for b, w in item_tags[j].items():
        nj += w * w
    if ret == 0:
        return 0
    return(ret / math.sqrt(ni * nj))
    
def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0
    for i in recommend_items.keys():
        for j in recommend_items.keys():
            if i == j:
                continue
            ret += CosineSim(item_tags, i, j)
            n += 1
    return(ret / (n * 1.0))

def addValueToMat(records, names, index, value = 1):
    a = pd.DataFrame(zip(records.keys(),
                         [y for x in records.values() for y in x.keys()],
                          [y for x in records.values() for y in x.values()]),
                          columns = names)
    drop_name = [i for i in names if i not in index]
    a[drop_name] = 1
    key = index[0]
    index_tag = index[1]
    b = {k: g.set_index(index_tag)[drop_name[0]].to_dict() for k,g in a.groupby(key)}
    return(b)
        
def Recommendation(records, user):
    recommend_items = dict()
    user_tags = addValueToMat(records, ['UserID', 'ItemID', 'TagID'], ['UserID', 'TagID'])
    tag_items = addValueToMat(records, ['UserID', 'ItemID', 'TagID'], ['TagID', 'ItemID'])
    user_items = addValueToMat(records, ['UserID', 'ItemID', 'TagID'], ['UserID', 'ItemID'])
    tagged_items = user_items[user]
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            #if items have been tagged, do not recommend them
            if tagged_items.has_key(item):
                continue
            if item not in recommend_items:
                recommend_items[item] = wut * wti
            else:
                recommend_items[item] += wut * wti
    return(recommend_items)