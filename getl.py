# -*- coding: utf-8 -*-

path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor\dblp1/'
for year in range(1981, 2000-1, 1):
    fn1 = path + str(year) + '-' + str(year ) + 'weight.txt'
    fn2 = path + str(year+1) + '-' + str(year +1) + 'weight.txt'
    fin1 = open(fn1)
    fin2 = open(fn2)
    edges_1 = set()
    edges_2 = set()
    nodes1 = set()
    nodes2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        nodes1.add(u)
        nodes1.add(v)
        edges_1.add((u,v))
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        nodes2.add(u)
        nodes2.add(v)
        edges_2.add((u,v))
    fin1.close()
    fin2.close()
    print len(edges_1 - edges_2), len(edges_1), float(len(edges_1 - edges_2))/len(edges_1)
    print len(nodes1 - nodes2), len(nodes1), float(len(nodes1 - nodes2))/len(nodes1)
    print '-------------------------------'

'''path = 'C:\Users\cc\Desktop/facebook-wall/facebook3/'
interval = 3
for months in range(2007*12, 2009*12, interval):
    next = months+interval
    fn = path + str(months/12*100+months%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1)
    fin1 = open(fn + '-commont1.txt')
    fin2 = open(fn + '-commont2.txt')
    edges_1 = set()
    edges_2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_1.add((u,v))
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_2.add((u,v))
    fin1.close()
    fin2.close()
    print len(edges_1 - edges_2), ',' '''

'''path = 'D:\imdb_b\imdb1/'
for year in range(1990, 1996, 1):
    fn1 = path + str(year) + '-' + str(year + 2-1) + '-commont1.txt'
    fn2 = path + str(year) + '-' + str(year + 2-1) + '-commont2.txt'
    fin1 = open(fn1)
    fin2 = open(fn2)
    edges_1 = set()
    edges_2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_1.add((u,v))
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_2.add((u,v))
    fin1.close()
    fin2.close()
    print len(edges_1 - edges_2), ','
    '''