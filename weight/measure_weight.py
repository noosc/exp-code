
import math
import networkx as nx
import numpy as np


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
        for y in neig[x]:
            degree[x]+=neig[x][y]
    return degree
        
        
## fn1 is the file in dblp_weight
## fn2 is the file in dblp5
def cal_CN_weight(fn1,fn2):
    neig=get_neig(fn1)
    edges=read_edges(fn2)
    sth={edge:0 for edge in edges}
    for x in sth:       
        for a in neig[x[0]]:
            for b in neig[x[1]]:
                if a==b:
                    sth[x]+=neig[x[0]][a]+neig[x[1]][a]
#    print sth

    return sth

def cal_AA_weight(fn1,fn2):
    neig=get_neig(fn1)
    degree=get_degree(fn1)
    edges=read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        for a in neig[x[0]]:
            for b in neig[x[1]]:
                if a==b:
                    sth[x]+=(neig[x[0]][a]+neig[x[1]][a])/(math.log(1+degree[a]))
#    print sth
    return sth

def cal_RA_weight(fn1,fn2):
    neig=get_neig(fn1)
    edges=read_edges(fn2)
    degree=get_degree(fn1)
    sth={edge:0. for edge in edges}
    for x in sth:
        for a in neig[x[0]]:
            for b in neig[x[1]]:
                if a==b:
                    sth[x]+=float(neig[x[0]][a]+neig[x[1]][a])/(degree[a])
#    print sth
    return sth

## reverse=True
def cal_PA_weight(fn1,fn2):

    edges=read_edges(fn2)
    degree=get_degree(fn1)
    sth={edge:0 for edge in edges}
    for x in sth:
        sth[x]=degree[x[0]]*degree[x[1]]
    return sth

def cal_JC_weight(fn1,fn2):
    neig=get_neig(fn1)
    edges=read_edges(fn2)
    degree=get_degree(fn1)
    sth={edge:0. for edge in edges}
    for x in sth:
        for a in neig[x[0]]:
            for b in neig[x[1]]:
                if a==b:
                    sth[x]+=float(neig[x[0]][a]+neig[x[1]][a])/(degree[x[0]]+degree[x[1]])

    return sth

## reverse=False
def cal_PA_weight_extend(fn1,fn2):
    sth={}
    degree=get_degree(fn1)
    for line in open(fn2):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        weight=int(x[2])
        if weight==1:
            sth[(u,v)]=-1
        elif((degree[u]==1) or (degree[v]==1)):
            sth[(u,v)]=-1
        else:
            sth[(u,v)]=1.0*weight/(degree[u]*degree[v])

    return sth

def cal_weight(fn1,fn2):
    sth={}
    edges = {}
    nodes = {}
    nei = {}
    for line in open(fn2):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        w=int(x[2])
        edges[(u,v)] = w
        nodes[u] = nodes.get(u,0) + w
        nodes[v] = nodes.get(v,0) + w
        if u not in nei:
            nei[u] = set()
        if v not in nei:
            nei[v] = set()
        nei[u].add(v)
        nei[v].add(u)

    for e in edges:
        sth[e] =edges[e]*100+nodes[e[0]] + nodes[e[1]]
    return sth

def cal_w(fn):
    sth={}
    edges = [{} for f in fn]
    nodes = [{} for f in fn]
    nei = {}
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
            if u not in nei:
                nei[u] = set()
            if v not in nei:
                nei[v] = set()
            nei[u].add(v)
            nei[v].add(u)

    nn = {}
    for k in range(5):
        for n in nodes[k]:
            s = []
            for j in range(5):
                s.append(nodes[4-j].get(n,0))
            nn[n] = s

    for e in edges[4]:
        sth[e] =edges[4][e]*849+(5-nn[e[0]].count(0) + 5-nn[e[1]].count(0))*170 + (nn[e[0]][1] + nn[e[1]][1])*21
    return sth


def cal_degree_ratio_weight(fn1,fn2):
    edges=read_edges(fn2)
    degree=get_degree(fn1)
    sth={edge:0 for edge in edges}

    for x in sth:
        i=degree[x[0]]
        j=degree[x[1]]
        if (i<=j):
            sth[x]=float(i)/j
        else:
            sth[x]=float(j)/i
#    print sth
    return sth

## error---solution:is not None---------------------------------------------
def cal_edge_betweenness(fn1,fn2):
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    
    G=nx.Graph()
    edges_all=prep.read_edges(fn1)
    G.add_edges_from(edges_all)
    edge_betweenness=nx.edge_betweenness_centrality(G)

    for x in sth.keys():
        u=(x[0], x[1])#!!!!!there is a blank between two nodes in edge_betweenness, so here need a switch
        if edge_betweenness.get(u) is not None:
            sth[x]=edge_betweenness.get(u)
        else:
            sth[x]=0
 
    return sth

## error:is not connected---solution: nx.connected_component_subgraphs(G)---        
def cal_edge_current_flow_betweenness_centrality(fn1,fn2):
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    
    G=nx.Graph()
    edges_all=prep.read_edges(fn1)
    G.add_edges_from(edges_all)

    graphs=list(nx.connected_component_subgraphs(G))#
    for g in graphs:
        edge_flow=nx.edge_current_flow_betweenness_centrality(
        g,normalized=True, weight=None,dtype=np.float32)
        for x in edge_flow.keys():
            if edge_flow.get(x) is not None:
                sth[x]=edge_flow.get(x)
    return sth
    

## fn1 is the file in dblp2
## fn2 is the file in dblp3
def cal_embed(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0 for edge in edges}
    for x in sth:
        common_neig=len(neig[x[0]] & neig[x[1]])
        if common_neig==0:
            sth[x]=0.0
        else:
            sth[x]=float(common_neig)/((len(neig[x[0]])-1)+(len(neig[x[1]])-1)-common_neig)
    return sth

def cal_clust(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    all_edges=prep.read_edges(fn1)
    sth={edge:0 for edge in edges}
    for x in sth:
        edges_among_neig_i=0
        neig_i=neig[x[0]]
        for edge in all_edges:
            if (edge[0] in neig_i) & (edge[1] in neig_i):
                edges_among_neig_i=edges_among_neig_i+1
        if edges_among_neig_i==0:
            Clust_i=0
        else:
            Clust_i=2.0*edges_among_neig_i/(len(neig[x[0]])*(len(neig[x[0]])-1))

        edges_among_neig_j=0
        neig_j=neig[x[1]]
        for edge in all_edges:
            if (edge[0] in neig_j) & (edge[1] in neig_j):
                edges_among_neig_j=edges_among_neig_j+1
        if edges_among_neig_i==0:
            Clust_i=0
        else:
            Clust_j=2.0*edges_among_neig_j/(len(neig[x[1]])*(len(neig[x[1]])-1))
        sth[x]=Clust_i*Clust_j

        return sth
    
def cal_triangles(fn1,fn2):
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    
    G=nx.Graph()
    edges_all=prep.read_edges(fn1)
    G.add_edges_from(edges_all)

    for x in sth:
        n1=nx.triangles(G,x[0])
        n2=nx.triangles(G,x[1])

        n3=max(n1,n2)
        n4=min(n1,n2)
        
        sth[x]=float(n4)/(n3+1)
##        sth[x]=(n1+1)*(n2+1)
##        sth[x]=n1+n2

    return sth

def cal_communicability_centrality(fn1,fn2):
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
   
    G=nx.Graph()
    edges_all=prep.read_edges(fn1)
    G.add_edges_from(edges_all)
    communicability=nx.communicability_centrality(G)

    for x in sth:
        n1= communicability.get(x[0])
        n2= communicability.get(x[1])
        print n1,n2
        n3=max(n1,n2)
        n4=min(n1,n2)
        sth[x]=float(n4)/(n3+1)
#        sth[x]=n1*n2
#        sth[x]=n1+n2
    return sth                                                         

if __name__=='__main__':
##    fn1='C:/Users/Administrator/Desktop/data/missing/dblp3/2/1980-1985-common.txt'
##    fn2='C:/Users/Administrator/Desktop/data/missing/dblp4/2/1980-1985-common.txt'
    fn1='C:/Users/Administrator/Desktop/data/missing/test11.txt' #time1
    fn2='C:/Users/Administrator/Desktop/data/missing/test11test.txt'
 
#    cal_AA_weight(fn1,fn2)
#    cal_RA_weight(fn1,fn2)
    cal_degree_ratio_weight(fn1,fn2)
    
##    cal_degree_ratio(fn1,fn2)
##    cal_embed(fn2,fn1)
##    cal_clust(fn2,fn1)
##    cal_AA(fn2,fn1)
##    cal_edge_betweenness(fn1,fn2)
##    cal_edge_current_flow_betweenness_centrality(fn1,fn2)
##    cal_triangles(fn1,fn2)
##    cal_communicability_centrality(fn1,fn2)
