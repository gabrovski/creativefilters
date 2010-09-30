#####
import re
import urllib2

BINGBASE = 'http://www.bing.com/search?q='
BINGEND = '&go=&form=QBRE&filt=all'
WEBSITE = 'opentable.com'

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
            res.insert(0, x)
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

if __name__ == '__main__':
    a = getRest('restaurants.csv')
    a = filterNames(a)
    r = lookUp(a[2][0]+a[2][len(a[2])-1],WEBSITE,BINGBASE, BINGEND)
    print getLink(r, '(http://www.opentable.*?)\"')
