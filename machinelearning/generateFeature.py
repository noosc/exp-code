# -*- coding: utf-8 -*-
import time
import os
import os.path

## f is file from dblp_weight
## ft is file from dblp_time
## fw is file write to dblp_feature
def preprocess(f,ft,fw,f2):

    edges=read_edges(f)
    
    isExist={edge: 0 for edge in edges}
    if f2!='':
        edges2=read_edges(f2)
        for edge in edges:
            if edge in edges2:
                isExist[edge]=1
     
    CN={edge:0 for edge in edges} ## record the number of common neigs of (u,v)
    CNWeight={edge:0 for edge in edges}   ## record CN_weight score of (u,v)
    
    RA={edge:0. for edge in edges}
    RAWeight={edge:0. for edge in edges}
    
    JC={edge:0. for edge in edges}
    JCWeight={edge:0. for edge in edges}
    
    Embed={edge:0. for edge in edges}
    EmbedWeight={edge:0. for edge in edges}
    
    PA={edge:0 for edge in edges}
    PAWeight={edge:0 for edge in edges}
    
    DegreeRatio={edge:0. for edge in edges}
    DegreeRatioWeight={edge:0. for edge in edges}

    firstCorp={}
    lastCorp={}
    timePeriod={}
    
    ## neig={1: {2: 3}, 2: {1: 3, 3: 2}, 3: {2: 2, 5: 1}, 4: {5: 2},
    ##    5: {8: 1, 3: 1, 4: 2, 6: 1}, 6: {5: 1}, 8: {5: 1}}    
    neig=get_neig(f)
    ## record the degree of every node in file f 
    degree=get_degree(f)
    degreeWeight=get_degree_weight(f)

    for line in open(f):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        t=int(x[2])

        for a in neig[u]:
            for b in neig[v]:
                if a==b:
                    
                    CN[(u, v)]+=1
                    CNWeight[(u, v)]+=neig[u][a]+neig[v][a]

                    RA[(u, v)]+=1.0/(degree[a])
                    RAWeight[(u, v)]+=float(neig[u][a]+neig[v][a])/(degreeWeight[a])
                                        
                    JCWeight[(u, v)]+=float(neig[u][a]+neig[v][a])/(degreeWeight[u]+degreeWeight[v])

        JC[(u, v)]+=float(CN[(u, v)])/(degree[u]+degree[v])
        PA[(u, v)]=degree[u]*degree[v]
        PAWeight[(u, v)]=degreeWeight[u]*degreeWeight[v]
        
        i=degree[u]
        j=degree[v]
        if (i<=j):
            DegreeRatio[(u, v)]=float(i)/j
        else:
            DegreeRatio[(u, v)]=float(j)/i
            
        iW=degreeWeight[u]
        jW=degreeWeight[v]
        if (iW<=jW):
            DegreeRatioWeight[(u, v)]=float(iW)/jW
        else:
            DegreeRatioWeight[(u, v)]=float(jW)/iW
        

    for line in open(f):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        if ((degree[u]-1)+(degree[v]-1)-CN[(u,v)])==0:
            Embed[(u,v)]=0
        else:
            Embed[(u,v)]=float(CN[(u,v)])/((degree[u]-1)+(degree[v]-1)-CN[(u,v)])

        if ((degreeWeight[u]-1)+(degreeWeight[v]-1)-CNWeight[(u,v)])==0:
            EmbedWeight[(u,v)]=0
        else:
            EmbedWeight[(u,v)]=float(CNWeight[(u,v)])/((degreeWeight[u]-1)+(degreeWeight[v]-1)-CNWeight[(u,v)])

## generate features: firstCorp, lastCorp, timePeriod  from file from dblp_time
    for line in open(ft):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        firstCorp[(u,v)]=int(x[2])
        lastCorp[(u,v)]=int(x[3])
        timePeriod[(u,v)]=int(x[4])
        
    print len(edges)
    fout=open(fw,'w')
    for i in edges:
        fout.write(str(i[0])+'\t'+str(i[1])+'\t'+str(degree[i[0]])+'\t'+str(degree[i[1]])+'\t')
        fout.write(str(PA[i])+'\t'+str(PAWeight[i])+'\t'+str(DegreeRatio[i])+'\t'+str(DegreeRatioWeight[i])
                   +'\t'+str(CN[i])+'\t'+str(CNWeight[i])+'\t')
        fout.write(str(RA[i])+'\t'+str(RAWeight[i])+'\t'+str(JC[i])+'\t'+str(JCWeight[i])+'\t'
                   +str(Embed[i])+'\t'+str(EmbedWeight[i])+'\t'+str(neig[i[0]][i[1]])+'\t')
        fout.write(str(firstCorp[i])+'\t'+str(lastCorp[i])+'\t'+str(timePeriod[i])+'\t'+str(isExist[i])+'\n')
    fout.close()

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

## fn is the file in dblp_weight
## neig={1: {2: 3}, 2: {1: 3, 3: 2}, 3: {2: 2, 5: 1}, 4: {5: 2},
##    5: {8: 1, 3: 1, 4: 2, 6: 1}, 6: {5: 1}, 8: {5: 1}}
def get_neig(fn):    
    all_nodes=read_nodes(fn)

    neig={}  ## neighbor of all_nodes        
    for x in all_nodes:
        neig[x]={}       
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        weight=int(x[2])
        if (neig[u].has_key(v)==False):
            neig[u][v]=0            
        if (neig[v].has_key(u)==False):
            neig[v][u]=0
        neig[u][v]+=weight
        neig[v][u]+=weight

    return neig                    

## fn is the file in dblp_weight
def get_degree(fn):
    neig=get_neig(fn)
    degree={node:0 for node in neig}
    for x in neig:
        degree[x]=len(neig[x])
    return degree

## fn is the file in dblp_weight
def get_degree_weight(fn):
    neig=get_neig(fn)
    degree={node:0 for node in neig}
    for x in neig:
        for y in neig[x]:
            degree[x]+=neig[x][y]
    return degree        

def write_file(path,interval):
    last = ''
    for year in range(1971, 2005-interval-1, interval):
        f1 = path + str(year) + '-' + str(year + interval-1)
        last = path + str(year + interval) + '-' + str(year + interval*2-1)
        f2 = last + 'weight.txt'
        if year + interval*2-1 > 2014:
            f2 = path + str(year + interval) + '-2014weight.txt'
        preprocess(f1 + 'weight.txt',f1 + 'time.txt',f1 + '-fl.txt',f2)
    preprocess(last + 'weight.txt',last + 'time.txt',last + '-fl.txt','')

def generate(fn,f2,fw):
    edges = [{} for f in fn]
    nodes = [{} for f in fn]
    for i in range(len(fn)):
        nei = {}
        for line in open(fn[i]):
            x=str(line).split('\t')
            u=int(x[0])
            v=int(x[1])
            w=int(x[2])
            edges[i][(u,v)] = w
            nodes[i][u] = nodes[i].get(u,0) + w
            nodes[i][v] = nodes[i].get(v,0) + w

    nn = {}
    for k in range(5):
        for n in nodes[k]:
            s = []
            for j in range(5):
                s.append(nodes[4-j].get(n,0))
            nn[n] = s

    isExist={edge: 0 for edge in edges[4]}
    if f2!='':
        edges2=read_edges(f2)
        for edge in edges[4]:
            if edge in edges2:
                isExist[edge]=1

    fout=open(fw,'w')
    for i in edges[4]:
        fout.write(str(i[0])+'\t'+str(i[1])+'\t')
        fout.write(str(edges[4][i]) + '\t' + str(5-nn[i[0]].count(0)) + '\t' + str(5-nn[i[1]].count(0)) + '\t')
        fout.write(str(isExist[i])+'\n')
    fout.close()

def write_file2(path,interval):
    last = ''
    for year in range(1981, 1990-interval-5, interval):
        fn = [path + str(year+interval*i) + '-' + str(year + interval*(i+1)-1) + 'weight.txt' for i in range(6)]
        fw = path + str(year+interval*4) + '-' + str(year + interval*(4+1)-1) + '-fl.txt'
        generate(fn[:5],fn[5],fw)

if __name__=='__main__':
    '''path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp5/'
    write_file(path,5)'''
    path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp1/'
    write_file2(path,1)

    


