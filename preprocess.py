# -*- coding: utf-8 -*-

import time
import datetime
import numpy as np
import os

def cut_file_dblp(inputfname,outputfname,timebegin,timeend,interval):
    fin = open(inputfname)
    fout_set = {}
    linknum = {}
    fin.readline()
    while True:
    	line = fin.readline()
    	if not line:
    		break
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        t = int(x[3])
        if u<v and t >= timebegin:
            year = datetime.datetime.fromtimestamp(t).strftime('%Y')
            begin = datetime.datetime.fromtimestamp(timebegin).strftime('%Y')
            year_2 = (int(year) - begin)/interval*interval +begin
            if year_2 not in fout_set:
                if year_2+interval-1 > timeend:
                    fout_set[year_2] = open(outputfname + str(year_2) + '-' + str(timeend) + '.txt', 'w')
                else:
                    fout_set[year_2] = open(outputfname + str(year_2) + '-' + str(year_2+interval-1) + '.txt', 'w')
            linknum[year_2] = linknum.get(year_2, 0) + 1
            fout = fout_set[year_2]
            fout.write(str(u)+'\t'+str(v)+'\t'+str(year)+'\n')
    fout = open(outputfname + 'distribution' + '.txt', 'w')
    for item in sorted(linknum.iteritems(), key = lambda d:d[0], reverse = False):
        if item[0]+interval-1 > timeend:
            fout.write(str(item[0]) + '-' + str(timeend) + str() + '\t' + str(item[1]) + '\n')
        else:
            fout.write(str(item[0]) + '-' + str(item[0]+interval-1) + '\t' + str(item[1]) + '\n')
    fout.close()
    for fp in fout_set.values():
        fp.close()
    fin.close()
    print 'ok'

def cut_file_fb(inputfname,outputfname,timebegin,interval):
    fin = open(inputfname)
    fout_set = {}
    linknum = {}
    begin_y = int(datetime.datetime.fromtimestamp(timebegin).strftime('%Y'))
    begin_m = int(datetime.datetime.fromtimestamp(timebegin).strftime('%m'))
    while True:
        line = fin.readline()
        if not line:
            break
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        t = int(x[2])
        if u!=v and t >= timebegin:
            current = datetime.datetime.fromtimestamp(t)
            year = int(current.year)
            month = int(current.month)
            day = int(current.day)
            key = ((year - begin_y)*12 + month-1)/interval*interval + begin_y*12
            if key not in fout_set:
                fout_set[key] = open(outputfname + str(key/12*100+key%12+1) + '-' + str((key+interval-1)/12*100+(key+interval-1)%12+1) + '.txt', 'w')
            linknum[key] = linknum.get(key, 0) + 1
            fout = fout_set[key]
            fout.write(str(u)+'\t'+str(v)+'\t'+str(year*10000+month*100+day)+'\n')
    for fp in fout_set.values():
        fp.close()
    fin.close()
    print 'ok'

def cut_file_fb2(inputfname,outputfname,timebegin,interval):
    fin = open(inputfname)
    fout_set = {}
    linknum = {}
    begin = datetime.datetime.fromtimestamp(timebegin)
    while True:
        line = fin.readline()
        if not line:
            break
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        t = int(x[2])
        if u!=v and t >= timebegin:
            current = datetime.datetime.fromtimestamp(t)
            year = int(current.year)
            month = int(current.month)
            day = int(current.day)
            key = begin + datetime.timedelta(days = (current-begin).days/interval*interval)
            if key not in fout_set:
                next = key + datetime.timedelta(days = interval-1)
                fout_set[key] = open(outputfname+str(key.year*10000+key.month*100+key.day)+'-'+str(next.year*10000+next.month*100+next.day)+'.txt','w')
            linknum[key] = linknum.get(key, 0) + 1
            fout = fout_set[key]
            fout.write(str(u)+'\t'+str(v)+'\t'+str(year*10000+month*100+day)+'\n')
    for fp in fout_set.values():
        fp.close()
    fin.close()
    print 'ok'

def cut_file_imdb(inputfname,outputfname,timebegin,timeend,interval):
    fin = open(inputfname)
    fout_set = {}
    for line in fin:
        x = str(line).split()
        u = int(x[0])
        v = int(x[1])
        year = int(x[2])
        year_2 = (year - timebegin)/interval*interval + timebegin
        if year_2 < timebegin or year_2 >= timeend:
            continue
        if year_2 not in fout_set:
            fout_set[year_2] = open(outputfname + str(year_2) + '-' + str(year_2+interval-1) + '.txt', 'w')
        fout = fout_set[year_2]
        fout.write(str(u)+'\t'+str(v)+'\t'+str(year)+'\n')

def cut_file_mail(inputfname,outputfname,begin,interval):
    fin = open(inputfname)
    fname = open(outputfname + 'filename.txt','w')
    fout_set = {}
    filenames = []
    linknum = {}
    while True:
        line = fin.readline()
        if not line:
            break
        x = str(line).split('\t')
        u = int(x[0])
        v = int(x[1])
        current = datetime.datetime.strptime(x[2][:-13],'%a, %d %b %Y %H:%M:%S')
        if u!=v and current >= begin:
            year = int(current.year)
            month = int(current.month)
            day = int(current.day)
            key = ((year - begin.year)*12 + month-1)/interval*interval + begin.year*12
            fn = outputfname + str(key/12*100+key%12+1) + '-' + str((key+interval-1)/12*100+(key+interval-1)%12+1) + '.txt'
            if key not in fout_set:
                filenames.append(fn)
                fout_set[key] = open(fn, 'w')
            fout = fout_set[key]
            linknum[fn] = linknum.get(fn,0) + 1
            fout.write(str(u)+'\t'+str(v)+'\t'+str(year*10000+month*100+day)+'\n')
    for fp in fout_set.values():
        fp.close()
    for fn in sorted(filenames):
        fname.write(fn + '\t' + str(linknum[fn]) + '\n')
    fname.close()
    fin.close()
    print 'ok'

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

def preprocess_file(fname1,fname2,fname3,fname4):
    nodes1 = read_nodes(fname1)
    nodes2 = read_nodes(fname2)
    nodes = nodes1 & nodes2

    fin1 = open(fname1)
    fout1 = open(fname3,'w')
    linknum1 = 0
    while True:
        line = fin1.readline()
        if not line:
            break
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)&(v in nodes):
            fout1.write(line)
            linknum1 += 1
    fin1.close()
    fout1.close()

    fin2 = open(fname2)
    fout2 = open(fname4,'w')
    linknum2 = 0
    while True:
        line = fin2.readline()
        if not line:
            break
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)&(v in nodes):
            fout2.write(line)
            linknum2 += 1
    fin1.close()
    fout1.close()

    print fname1 + ' has ' + str(linknum1) + ' edges with two common nodes'
    print fname2 + ' has ' + str(linknum2) + ' edges with two common nodes'

def preprocess2_file(fname1,fname2,fname3,fname4):
    nodes1 = read_nodes(fname1)
    nodes2 = read_nodes(fname2)
    nodes = nodes1 & nodes2

    fin1 = open(fname1)
    fout1 = open(fname3,'w')
    linknum1 = 0
    while True:
        line = fin1.readline()
        if not line:
            break
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)|(v in nodes):
            fout1.write(line)
            linknum1 += 1
    fin1.close()
    fout1.close()

    fin2 = open(fname2)
    fout2 = open(fname4,'w')
    linknum2 = 0
    while True:
        line = fin2.readline()
        if not line:
            break
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)|(v in nodes):
            fout2.write(line)
            linknum2 += 1
    fin1.close()
    fout1.close()

    print fname1 + ' has ' + str(linknum1) + ' edges with one common nodes'
    print fname2 + ' has ' + str(linknum2) + ' edges with one common nodes'

if __name__ == '__main__':
    '''a="1971-01-01 00:00:00"
    timeBegin=time.strptime(a,"%Y-%m-%d %H:%M:%S")
    timeStampBegin=int(time.mktime(timeBegin))
    fn='C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/out.dblp_coauthor'#out.dblp_coauthor
    fout='C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp'
    for interval in range(6):
        path = fout + str(interval+1) + '/'
        os.mkdir(path)
        cut_file_dblp(fn,path,timeStampBegin,2014,interval+1)
    a="2004-01-01 00:00:00"
    timeBegin=time.strptime(a,"%Y-%m-%d %H:%M:%S")
    timeStampBegin=int(time.mktime(timeBegin))
    fn = 'C:\Users\cc\Desktop/facebook-wall/facebook-wall.txt.anon'
    fout = 'C:\Users\cc\Desktop/facebook-wall/facebook'
    for interval in range(3):
        path = fout + str(interval+1) + '/'
        os.mkdir(path)
        cut_file_fb(fn,path,timeStampBegin,interval+1)
    for interval in range(10,31,10):
        path = fout + str(interval) + '/'
        os.mkdir(path)
        cut_file_fb2(fn,path,timeStampBegin,interval)'''
    '''fn='D:\imdb_b\imdb_b.txt'
    fout='D:\imdb_b\imdb'
    for interval in range(1):
        path = fout + str(interval+1) + '/'
        os.mkdir(path)
        cut_file_imdb(fn,path,1990,2005,interval+1)'''
    a="2000-01-01 00:00:00"
    timeBegin=datetime.datetime.strptime(a,"%Y-%m-%d %H:%M:%S")
    fn = 'C:\Users\cc\Desktop\mail\mails.txt'
    fout = 'C:\Users\cc\Desktop/mail/mail'
    for interval in range(3):
        path = fout + str(interval+1) + '/'
        os.mkdir(path)
        cut_file_mail(fn,path,timeBegin,interval+1)