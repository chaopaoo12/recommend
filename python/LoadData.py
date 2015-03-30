# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 17:51:48 2015

@author: Administrator
"""
import pandas as pd
import re
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

class LoadData():
    def __init__(self, path):
        self.path = path
        
    def load(self, path, sep, names = None):
        if names is None:
            data = pd.read_csv(filepath_or_buffer = path, sep = sep)
        else:
            data = pd.DataFrame(pd.read_csv(filepath_or_buffer = path, header= None, sep = sep))
        return(data)
        
    @exeTime
    def prepare(self, path, names, splitmark, sep):
        if splitmark is None:
            data = self.load(path = path, names = names, sep = sep)
        else:
            data = self.load(path = path, names = names, sep = sep )
            data = list(data[0].map(lambda x : x.split(splitmark)))
            data = pd.DataFrame(data, columns = names)
        return(data)
     
    @exeTime
    def getData(self, files, names, splitmark, sep = 'delimiter'):
        print(splitmark)
        data = locals()
        for i in range(len(files)):
            path = self.path +'\\'+ files[i] + '.dat'
            if names is None:
                
                data['data%s'  % i] = self.prepare(path = path, names = names, splitmark = splitmark, sep = sep)
            else:
                data['data%s'  % i] = self.prepare(path = path, names = names[i], splitmark = splitmark, sep = sep)
        returns = [key for key in data.keys() if re.findall(r"data\d", key)]
        return([data[key] for key in returns])
        
if __name__ == '__main__':
    data_path = 'G:\\pyhton\\recommended system\\dataset\\MovieLens'
    data = LoadData(data_path)
    files = ['users','movies','ratings']
    names = [['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'],
             ['MovieID', 'Title', 'Genres'],
             ['UserID','MovieID','Rating','Timestamp']]
    splitmark = '::'
    #exec(filename + '''=data.getData(files, splitmark, names)''')
    [Movies, Users, Ratings] = data.getData(files = files, splitmark = splitmark, names = names)