# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 09:31:36 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-
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
def foo():
	for i in xrange(10000000):
		pass

if __name__ == "__main__":
	foo()