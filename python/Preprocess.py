# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 14:52:24 2015

@author: Administrator
"""
import numpy as np
import time

# --exeTime
def exeTime(func):
	def newFunc(*args, **args2):
		t0 = time.time()
		print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
		back = func(*args, **args2)
		print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
		print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
		return back
	return newFunc
# --end of exeTime

@exeTime
def SplitData(data, names, index, M, k):
    test = []
    train = []
    num = np.floor(len(data)/10)
    res = len(data) - num * 10
    index1 = np.append(np.tile(np.linspace(1,10,10), num), np.linspace(1,res,res))
    train = data[index1 == k][names]
    test = data[index1 != k][names]
    key = names[index[0]]
    index_tag = names[index[1]]
    value_tag = names[index[2]]
    train = {k: g.set_index(index_tag)[value_tag].to_dict() for k,g in train.groupby(key)}
    test = {k: g.set_index(index_tag)[value_tag].to_dict() for k,g in test.groupby(key)}
    return(train, test)


if __name__ == '__main__':
    train,test = SplitData(Ratings,['UserID','MovieID','Rating'], [0,1,2], 10, 1)





#