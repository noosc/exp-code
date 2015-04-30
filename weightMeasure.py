import preprocess as prep
import math
import networkx as nx
import numpy as np

## fn1 is the file in dblp3
## fn2 is the file in dblp2
def cal_degree_ratio(fn1,fn2):
    edges=prep.read_edges(fn2)
    sth={edge:0 for edge in edges}
    
    all_nodes=prep.read_nodes(fn1)
    all_edges=prep.read_edges(fn1)
    neig={}  ## neighbor of all_nodes
    for x in all_nodes:
        neig[x]=set()
        
    for line in all_edges:
        u=line[0]
        v=line[1]
        neig[u].add(v)
        neig[v].add(u)

    for x in sth:
        i=len(neig[x[0]])
        j=len(neig[x[1]])
        if (i<=j):
            sth[x]=float(i)/j
        else:
            sth[x]=float(j)/i
    return sth

## fn is the file in dblp2
def get_neig(fn):    
    all_nodes=prep.read_nodes(fn)
    all_edges=prep.read_edges(fn)
    neig={}  ## neighbor of all_nodes
    for x in all_nodes:
        neig[x]=set()       
    for line in all_edges:
        u=line[0]
        v=line[1]
        neig[u].add(v)
        neig[v].add(u)
    return neig


## fn1 is the file in dblp2
## fn2 is the file in dblp3
def cal_CN(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0 for edge in edges}
    for x in sth:
        sth[x]=len(neig[x[0]] & neig[x[1]])
    return sth

def cal_AA(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        for z in (neig[x[0]] & neig[x[1]]):
            sth[x]+=1/(math.log(len(neig[z])))
    return sth

def cal_RA(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        for z in (neig[x[0]] & neig[x[1]]):
            sth[x]+=1/(len(neig[z]))
    return sth

## reverse=True
def cal_PA(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        sth[x]=len(neig[x[0]])*len(neig[x[1]])
    return sth

## reverse=False
def cal_PA_extend(fn1,fn2):
    neig=get_neig(fn1)
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        if ((len(neig[x[0]])==1) or (len(neig[x[1]])==1)):
            sth[x]=0.
        else:
            sth[x]=1.0/(len(neig[x[0]])*len(neig[x[1]]))
    return sth

## reverse=False
def cal_JC(fn1,fn2):
    neig=get_neig(fn1)
    #print neig
    edges=prep.read_edges(fn2)
    sth={edge:0. for edge in edges}
    for x in sth:
        if ((len(neig[x[0]])==1) or (len(neig[x[1]])==1)):
            sth[x] = 0
        else:
            sth[x]=float(len(neig[x[0]]&neig[x[1]]))/(len(neig[x[0]]|neig[x[1]])-2)
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
            Clust_j=0
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
    fn1='C:/Users/Administrator/Desktop/data/missing/test2.txt' #time1
    fn2='C:/Users/Administrator/Desktop/data/missing/time1test.txt'
    sth=cal_JC(fn1,fn2)
    print sth
    sth=cal_embed(fn1,fn2)
    print sth
    
#    cal_degree_ratio(fn1,fn2)
##    cal_embed(fn2,fn1)
##    cal_clust(fn2,fn1)
##    cal_AA(fn2,fn1)
##    cal_edge_betweenness(fn1,fn2)
##    cal_edge_current_flow_betweenness_centrality(fn1,fn2)
##    cal_triangles(fn1,fn2)
 #   cal_communicability_centrality(fn1,fn2)
