#####
import re

def getRest(inp):
    f = open(inp, 'r')
    t = f.readlines()[1:]
    f.close()

    for x in xrange(len(t)):
        t[x] = re.findall('\"(.*?)\"', t[x], re.U)
        #print t[x]
    return t

def filterNames(l):
    res = []
    for x in l:
        if x[0].rfind('\\x') == -1:
            res.insert(0, x)
    #print res
    return res

if __name__ == '__main__':
    a = getRest('restaurants.csv')
    print filterNames(a)
