# -*- coding: utf-8 -*-

import datetime

def get_common1(fname1,fname2,fname3,fname4):
    fin1 = open(fname1)
    fin2 = open(fname2)
    set1 = {}
    set2 = {}
    node_set1 = set()
    node_set2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        set1[(u,v)] = line
        node_set1.add(u)
        node_set1.add(v)
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        set2[(u,v)] = line
        node_set2.add(u)
        node_set2.add(v)
    fin1.close()
    fin2.close()
    node_set = node_set1 & node_set2
    fout1 = open(fname3,'w')
    for k in set1:
        if k[0] in node_set and k[1] in node_set:
            fout1.write(str(set1[k]))
    fout1.close()
    fout2 = open(fname4,'w')
    for k in set2:
        if k[0] in node_set and k[1] in node_set:
            fout2.write(str(set2[k]))
    fout2.close()

def get_common2(fname1,fname2,fname3,fname4):
    fin1 = open(fname1)
    fin2 = open(fname2)
    set1 = {}
    set2 = {}
    node_set1 = set()
    node_set2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        set1[(u,v)] = line
        node_set1.add(u)
        node_set1.add(v)
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        set2[(u,v)] = line
        node_set2.add(u)
        node_set2.add(v)
    fin1.close()
    fin2.close()
    node_set = node_set1 & node_set2
    fout1 = open(fname3,'w')
    for k in set1:
        if k[0] in node_set or k[1] in node_set:
            fout1.write(str(set1[k]))
    fout1.close()
    fout2 = open(fname4,'w')
    for k in set2:
        if k[0] in node_set or k[1] in node_set:
            fout2.write(str(set2[k]))
    fout2.close()

def get_info(fname1,fname2):
    fin1 = open(fname1)
    fin2 = open(fname2)
    edges_1 = set()
    edges_2 = set()
    node_set1 = set()
    node_set2 = set()
    for line in fin1.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_1.add((u,v))
        node_set1.add(u)
        node_set1.add(v)
    for line in fin2.readlines():
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        edges_2.add((u,v))
        node_set2.add(u)
        node_set2.add(v)
    fin1.close()
    fin2.close()
    miss_ratio=float(len(edges_1-edges_2))/len(edges_1)
    new_ratio=float(len(edges_2-edges_1))/len(edges_1)
    return fname1.split('/')[-1][:9] + '\t' + str(len(node_set1)) + '\t' + str(len(edges_1)) + '\t' + str(miss_ratio) + '\t' + str(new_ratio) + '\n'

if __name__ == '__main__':
    '''text = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp'
    for interval in range(6):
        path = text + str(interval+1) + '/'
        fout = open(path+'distribution.txt','w')
        for year in range(1971, 2015-interval-1, interval+1):
            fn1 = path + str(year) + '-' + str(year + interval)
            fn2 = path + str(year+interval+1) + '-' + str(year + interval*2+1)
            fn3 = path + str(year) + '-' + str(year + interval*2+1)
            if year + interval*2+1 > 2014:
                fn2 = path + str(year+interval+1) + '-2014'
                fn3 = path + str(year) + '-2014'
            fout.write(get_info(fn1 + 'weight.txt',fn2 + 'weight.txt'))
            #get_common1(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw1.txt', fn3 + '-commonw2.txt')
            #get_common1(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont1.txt', fn3 + '-commont2.txt')
            #get_common2(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw3.txt', fn3 + '-commonw4.txt')
            #get_common2(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont3.txt', fn3 + '-commont4.txt')
        fout.close()'''

    '''text = 'C:\Users\cc\Desktop/facebook-wall/facebook'
    for interval in range(1,4):
        path = text + str(interval) + '/'
        for months in range(2004*12+9/interval*interval, 2009*12, interval):
            fn1 = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1)
            next = months+interval
            fn2 = path + str(next/12*100+next%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1)
            fn3 = path + str(months/12*100+months%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1)
            get_common1(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw1.txt', fn3 + '-commonw2.txt')
            get_common1(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont1.txt', fn3 + '-commont2.txt')
            get_common2(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw3.txt', fn3 + '-commonw4.txt')
            get_common2(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont3.txt', fn3 + '-commont4.txt')
    first = datetime.datetime(2004, 10, 14)
    begin = datetime.datetime(2004, 1, 1)
    end = datetime.datetime(2009, 1, 22)
    for interval in range(10,31,10):
        path = text + str(interval) + '/'
        for days in range((first-begin).days/interval*interval, (end-begin).days-interval, interval):
            date = begin + datetime.timedelta(days = days)
            nextdate = date + datetime.timedelta(days = interval-1)
            next = date + datetime.timedelta(days = interval)
            nextnext = next + datetime.timedelta(days = interval-1)
            fn1 = path + str(date.year*10000+date.month*100+date.day) + '-' + str(nextdate.year*10000+nextdate.month*100+nextdate.day)
            fn2 = path + str(next.year*10000+next.month*100+next.day) + '-' + str(nextnext.year*10000+nextnext.month*100+nextnext.day)
            fn3 = path + str(date.year*10000+date.month*100+date.day) + '-' + str(nextnext.year*10000+nextnext.month*100+nextnext.day)
            get_common1(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw1.txt', fn3 + '-commonw2.txt')
            get_common1(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont1.txt', fn3 + '-commont2.txt')
            get_common2(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw3.txt', fn3 + '-commonw4.txt')
            get_common2(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont3.txt', fn3 + '-commont4.txt')

    text = 'D:\imdb_b\imdb'
    for interval in range(1):
        path = text + str(interval+1) + '/'
        fout = open(path+'distribution.txt','w')
        for year in range(1990, 2005-interval-1, interval+1):
            fn1 = path + str(year) + '-' + str(year + interval)
            fn2 = path + str(year+interval+1) + '-' + str(year + interval*2+1)
            fn3 = path + str(year) + '-' + str(year + interval*2+1)
            fout.write(get_info(fn1 + 'weight.txt',fn2 + 'weight.txt'))
            get_common1(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw1.txt', fn3 + '-commonw2.txt')
            get_common1(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont1.txt', fn3 + '-commont2.txt')
            get_common2(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw3.txt', fn3 + '-commonw4.txt')
            get_common2(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont3.txt', fn3 + '-commont4.txt')
        fout.close()'''

    text = 'C:\Users\cc\Desktop/mail/mail'
    for interval in range(1,2):
        path = text + str(interval) + '/'
        for months in range(2001*12+4/interval*interval, 2002*12+1, interval):
            fn1 = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1)
            next = months+interval
            fn2 = path + str(next/12*100+next%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1)
            fn3 = path + str(months/12*100+months%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1)
            get_common1(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw1.txt', fn3 + '-commonw2.txt')
            get_common1(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont1.txt', fn3 + '-commont2.txt')
            get_common2(fn1 + 'weight.txt',fn2 + 'weight.txt', fn3 + '-commonw3.txt', fn3 + '-commonw4.txt')
            get_common2(fn1 + 'time.txt',fn2 + 'time.txt', fn3 + '-commont3.txt', fn3 + '-commont4.txt')