# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:43:02 2015

@author: Administrator
"""

import math
from Preprocess import exeTime

class Evaluate():
    
    def __init__(self, test):
        self.test = test
    
    def setParam(self, reco):
        self.reco = reco
        self.train = reco.train
        return(self)
        
    def GetRecommendation(self, reco, user, N):
        Rank = reco.Recommendation(user, N)
        return(Rank)
        
    #召回率
    @exeTime
    def Recall(self, N):        
        hit = 0
        allnum = 0
        for user in self.train.keys():
            tu = self.test[user]
            rank = self.GetRecommendation(self.reco, user, N)
            for item, pui in rank:
                if item in tu:
                    hit += 1
            allnum += len(tu)
        return(hit / (allnum * 1.0))
    
    #准确率
    @exeTime
    def Precision(self, N):
        hit = 0
        allnum = 0
        for user in self.train.keys():
            tu = self.test[user]
            rank = self.GetRecommendation(self.reco, user, N)
            for item, pui in rank:
                if item in tu:
                    hit += 1
            allnum += N
        return(hit / (allnum * 1.0))
        
    #覆盖率
    @exeTime
    def Coverage(self, N):
        recommend_items = set()
        all_items = set()
        for user in self.train.keys():
            for item in self.train[user].keys():
                all_items.add(item)
                rank = self.GetRecommendation(self.reco, user, N)
            for item, pui in rank:
                recommend_items.add(item)
        return(len(recommend_items) / (len(all_items) * 1.0))
        
    #新颖度
    @exeTime
    def Popularity(self, N):
        item_popularity = dict()
        for user, items in self.train.items():
            for item in items.keys():
                if item not in item_popularity:
                    item_popularity[item] = 0
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in self.train.keys():
            rank = self.GetRecommendation(self.reco, user, N)
            for item, pui in rank:
                ret += math.log(1 + item_popularity[item])
                n += 1
        ret /= n * 1.0
        return(ret)
        
    @exeTime               
    def result(self, N):
        Recall = self.Recall(N)
        Precision = self.Precision(N)
        Coverage = self.Coverage(N)
        Popularity = self.Popularity(N)
        re = {'Recall' : Recall,'Precision': Precision,'Coverage' : Coverage,'Popularity' : Popularity}
        return(re)
        
if __name__ == '__main__':
    Eva = Evaluate(test)
    UserEva = Eva.setParam(UserReco)
    UserEva = UserEva.result(10)
    ItemEva = Eva.setParam(ItemReco)
    ItemEva = ItemEva.result(10)