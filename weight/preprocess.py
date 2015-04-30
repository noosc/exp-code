# -*- coding: utf-8 -*-

import preprocess as prep
import math
import networkx as nx
import numpy as np
import datetime

def read_nodes(fn):
    f=open(fn)
    nodes=set()
    for line in f:
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        nodes.add(u)
        nodes.add(v)
    f.close()
    return nodes

def read_edges(fn):
    f=open(fn)
    edges=set()
    for line in f:
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        edges.add((u,v))
    f.close()
    return edges

#indexed from 0
def build_net(edges):
    dim = 0
    for x in edges:
        if x[1] > dim:
            dim = x[1]
    print dim       
    mat = np.zeros((dim, dim), dtype = np.int)
    for x in edges:
        u = x[0] - 1
        v = x[1] - 1
        mat[u][v] = mat[v][u] = 1
    return mat

def cal_wight(fname1,fname2):
    fin = open(fname1)
    weight = {}
    while True:
        line = fin.readline()
        if not line:
            break
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        weight[(u,v)] = weight.get((u,v), 0) + 1
    fout = open(fname2, 'w')
    for (k,v) in weight.items():
        fout.write(str(k[0]) + '\t' + str(k[1]) + '\t' + str(v) + '\n')
    fin.close()
    fout.close()

if __name__ == '__main__':
    '''text = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp'
    for interval in range(6):
    	path = text + str(interval+1) + '/'
    	for year in range(1971, 2015, interval+1):
    		if year + interval > 2014:
    			fn = path + str(year) + '-2014'
    		else:
    			fn = path + str(year) + '-' + str(year + interval)
    		cal_wight(fn + '.txt', fn + 'weight.txt')'''

    '''text = 'C:\Users\cc\Desktop/facebook-wall/facebook'
    for interval in range(1,4):
        path = text + str(interval) + '/'
        for months in range(2004*12+9/interval*interval, 2009*12+1, interval):
            fn = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1)
            cal_wight(fn + '.txt', fn + 'weight.txt')
    first = datetime.datetime(2004, 10, 14)
    begin = datetime.datetime(2004, 1, 1)
    end = datetime.datetime(2009, 1, 22)
    for interval in range(10,31,10):
        path = text + str(interval) + '/'
        for days in range((first-begin).days/interval*interval, (end-begin).days+1, interval):
            date = begin + datetime.timedelta(days = days)
            nextdate = date + datetime.timedelta(days = interval-1)
            fn = path + str(date.year*10000+date.month*100+date.day) + '-' + str(nextdate.year*10000+nextdate.month*100+nextdate.day)
            cal_wight(fn + '.txt', fn + 'weight.txt')

    text='D:\imdb_b\imdb'
    for interval in range(1):
        path = text + str(interval+1) + '/'
        for year in range(1990, 2005, interval+1):
            fn = path + str(year) + '-' + str(year + interval)
            cal_wight(fn + '.txt', fn + 'weight.txt')'''

    text = 'C:\Users\cc\Desktop/mail/mail'
    for interval in range(1,2):
        path = text + str(interval) + '/'
        for months in range(2001*12+4/interval*interval, 2002*12+2, interval):
            fn = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1)
            cal_wight(fn + '.txt', fn + 'weight.txt')