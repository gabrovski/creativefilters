'''
Created on Jul 14, 2010

@author: Sasho

A threaded scraper for a list of urls. A new approach :)
'''

import urllib
import time
import pickle
import Queue
from threading import Thread
import sys

class Scrape(Thread):
    def __init__(self, urls, indx, dir, prefix=''):
        Thread.__init__(self)
        self.urls = urls
        self.i = indx
        self.dir = dir
        self.prf = prefix
        
    def run(self):
        for u in self.urls:
            f = urllib.urlopen(self.prf+u)
            txt = f.read()
            f.close()
            time.sleep(1)

            w = open(self.dir+'/'+(str(self.i)+'.html'), 'w')
            w.write(txt)
            w.close()
            self.i = self.i+1
            
class Scrape2(Thread):
    def __init__(self, queue, dir, prefix='', sleep=0):
        Thread.__init__(self)
        self.queue = queue
        self.dir = dir
        self.prf = prefix
        self.sleep = sleep
        
    def run(self):
        while True:
            try:
                u = self.queue.get()
                f = urllib.urlopen(self.prf+u[0])
                txt = f.read()
                f.close()
                time.sleep(self.sleep)
    
                w = open(self.dir+'/'+(str(u[1])+'.html'), 'w')
                w.write(self.prf+u[0])
                w.write('\n\n\n')
                w.write(txt)
                w.close()
                
                print "Got", u[0], "from", self.queue.qsize()
                self.queue.task_done()
            except KeyboardInterrupt:
                self.queue.task_done()
                sys.exit()
                
            
def splitter(lst, size):
    res = []
    curr = 0
    while curr < len(lst):
        res.append((lst[curr:curr+size],curr))
        curr = curr + size
    return res
        
#a = list(range(0,30))
#for x in splitter(a, 3):
#    print x
    
def scrape(dir, size, lst):
    scrlist = []
    dtalist = splitter(lst, size)
    for d in dtalist:
        current = Scrape(d[0], d[1], dir, prefix='http://www.yelp.com')
        scrlist.append(current)
        current.start()
        
    for s in scrlist:
        s.join()
        print "Scrape %d is done" % s.i
        
def scrape2(dir, size, lst, pref, sleep=0):
    lst = zip(lst, list(xrange(len(lst))))
    q = Queue.Queue()
    for i in xrange(size):
        t = Scrape2(q, dir, prefix=pref, sleep=sleep)
        t.setDaemon(True)
        t.start()
        
    map(q.put, lst)
    q.join()
    print "Done"
        
#f = open("testdir/lynks.pkl", 'rb')
#lst = pickle.load(f)
#f.close()
#
#print time.ctime()
#scrape2("testdir", 50, lst, 'http://www.yelp.com')
#print time.ctime()    
