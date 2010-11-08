#####
import re
import urllib2
import time
from threadScrape import scrape2

BINGBASE = 'http://www.bing.com/search?q='
BINGEND = '&go=&form=QBRE&filt=all'
WEBSITE = 'opentable'

def getRest(inp):
    f = open(inp, 'r')
    t = f.readlines()[1:]
    f.close()

    for x in xrange(len(t)):
        t[x] = re.findall('\"(.*?)\"', t[x])
        #print t[x]
    return t

def filterNames(l):
    res = []
    for x in l:
        if str(x[0]).rfind('\\x') == -1:
            res.append(x)
    #print res
    return res

#idetifief opentable.com as the website to use. will use google to get links to the restaurants. google api is not very good, important info often is not present in the available database (missing pages that can be found using the regular search engine). that's why will use google search engine in general with modification of the url so i get the real deal. 
#Correction:Use Bing
def lookUp(query, website, base, end):
    query = re.sub('[ \t]', '+', query)
    query = re.sub('[,\.\']', '', query)
    print query
    f = urllib2.urlopen(base+query+'+'+website+end)
    txt = f.read()
    f.close()
    #print txt
    return txt

def getLink(txt, s):
    m = re.search(s, txt)
    if m:
        return m.group(1)
    else:
        return None

def getAllLinks(inp, out):
    a = getRest(inp)
    a = filterNames(a)
    w = open(out, "w")
    for x in a:
        r = lookUp(x[0]+x[len(x)-1],WEBSITE,BINGBASE, BINGEND)
        l = getLink(r, '(http://www.opentable.*?)\"')
        if l:
            w.write(l)
            w.write('\n')
        time.sleep(1)
    w.close()

def revURL(directory, start, end):
    pass

if __name__ == '__main__':
    f = open("links.txt", "r")
    lst = f.readlines()
    for i in xrange(len(lst)):
        lst[i] = re.sub("\-reservatio.*", '', lst[i])
    f.close()
    #print lst
    scrape2("opentable", 50, lst, '')
