# -*- coding: utf-8 -*-
import math
import random
import numpy as np
import time
import datetime

##自dblp_feature_label文件夹生成，只有同时出现在t1和t2的节点
##保存在文件夹dblp_Feature_common文件夹中
def preprocess_file(fn1,fn2,fn3,fout1,fout2,fout3):
    nodes_in_file1=read_nodes(fn1)
    nodes_in_file2=read_nodes(fn2)
    nodes_in_file3=read_nodes(fn3)
    nodes=set()
    nodes=nodes_in_file1 & nodes_in_file2 & nodes_in_file3
    
    fw1=open(fout1,'w')
    num_of_links_1=0
    for line in open(fn1):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)&(v in nodes):
            fw1.write(line)
            num_of_links_1+=1
    fw1.close()

    fw2=open(fout2,'w')
    num_of_links_2=0
    for line in open(fn2):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)&(v in nodes):
            fw2.write(line)
            num_of_links_2+=1
    fw2.close()

    fw3=open(fout3,'w')
    num_of_links_3=0
    for line in open(fn3):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if (u in nodes)&(v in nodes):
            fw3.write(line)
            num_of_links_3+=1
    fw3.close()
    print fn1+" has "+str(num_of_links_1)+" edges with two common nodes"
    print fn2+" has "+str(num_of_links_2)+" edges with two common nodes"
    print fn3+" has "+str(num_of_links_3)+" edges with two common nodes"
 
def cal_miss_ratio(fn1,fn2):
    edges_1=read_edges(fn1)
    edges_2=read_edges(fn2)
    
    print "edges_1 "+str(len(edges_1))
    print "edges_2 "+str(len(edges_2))
    
    miss_ratio=float(len(edges_1-edges_2))/len(edges_1)
    new_ratio=float(len(edges_2-edges_1))/len(edges_1)

    print "miss links "+str(len(edges_1-edges_2))
    print "new links "+str(len(edges_2-edges_1))

    print "miss_ratio is "+str(miss_ratio)
    print "new added ratio is "+str(new_ratio)

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

if __name__=='__main__':

##    preprocess two files, keep the links with one commom node
    path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp5/'
    interval = 5
    for year in range(1971, 2005-interval*2-1, interval):
        fn1 = path + str(year) + '-' + str(year + interval-1)
        fn2 = path + str(year + interval) + '-' + str(year + interval*2-1)
        fn3 = path + str(year + interval*2) + '-' + str(year + interval*3-1)
        preprocess_file(fn1 + '-fl.txt',fn2 + '-fl.txt',fn3 + '-fl.txt',fn1 + '-flc1.txt',fn2 + '-flc2.txt',fn3 + '-flc3.txt')
        cal_miss_ratio(fn1 + '-flc1.txt',fn2 + '-flc2.txt')
        cal_miss_ratio(fn2 + '-flc2.txt',fn3 + '-flc3.txt')

