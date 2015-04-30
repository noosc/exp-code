import math
import string

#u    v    first coperation    last coperation    corperation period time    coperation year list   recent_u    recent_v

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

## fn_weight is the file in dblp_weight
## neig={1: {2: 3}, 2: {1: 3, 3: 2}, 3: {2: 2, 5: 1}, 4: {5: 2},
##    5: {8: 1, 3: 1, 4: 2, 6: 1}, 6: {5: 1}, 8: {5: 1}}
def get_neig(fn_weight):    
    all_nodes=read_nodes(fn_weight)

    neig={}  ## neighbor of all_nodes        
    for x in all_nodes:
        neig[x]={}       
    for line in open(fn_weight):
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

## fn_weight is the file in dblp_weight
def get_degree(fn_weight):
    neig=get_neig(fn_weight)
    degree={node:0 for node in neig}
    for x in neig:
        for y in neig[x]:
            degree[x]+=neig[x][y]
    return degree

def get_stardard_degree(fn_weight):
    degree=get_degree(fn_weight)
    stardard_degree={}
    max_degree=1
    min_degree=10
    for key in degree.keys():
        if degree[key]>max_degree:
            max_degree=degree[key]
        if degree[key]<min_degree:
            min_degree=degree[key]
    for key in degree.keys():
        stardard_degree[key]=(float)(max_degree-degree[key])/(max_degree-min_degree)

    return stardard_degree

#u    v    first coperation    last coperation    corperation period time    coperation year list   recent_u    recent_v
def cal_current_last_timespan(fn,currentTime):
    last={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])

        last[(u,v)]=1./(1+currentTime-int(x[3]))
    return last    

def cal_current_first_timespan(fn,currentTime):
    first={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
#        first[(u,v)]=currentTime-int(x[2])        
        first[(u,v)]=1./(1+currentTime-int(x[2]))
# choose one measure
    return first 

def cal_last_first_timespan(fn):
    timespan={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])        
        timespan[(u,v)]=int(x[4])
    return timespan 

# alpha=0.1  alpha always (0,1)
def cal_time_list(fn,currentTime,alpha):
    sth={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        sum=0.
        timeList=get_timeList(x[5])
        for i in timeList:
            sum+=math.pow((1-alpha),(currentTime-int(i)))/(currentTime-int(i)+1)
        sth[(u,v)]=sum
    return sth 

def cal_degree_timelist(fn_weight,fn,currentTime,alpha):
    sth={}
    degree=get_stardard_degree(fn_weight)
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        sum=0.
        timeList=get_timeList(x[5])
        for i in timeList:
            sum+=math.pow((1-alpha),(currentTime-int(i)))/(currentTime-int(i)+1)
        sth[(u,v)]=sum*math.pow(1.4,((degree[u]+1)*(degree[v]+1)))*((degree[u]+1)*(degree[v]+1))  #sum/.... is also good
    return sth
def cal_jc_timelist(fn_weight,fn,currentTime,alpha):
    sth={}
    degree=get_degree(fn_weight)
    neig=get_neig(fn_weight)
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        sum=0.
        timeList=get_timeList(x[5])
        for i in timeList:
            sum+=math.pow((1-alpha),(currentTime-int(i)))
        common=0
        for a in neig[u]:
            for b in neig[v]:
                if a==b:
                    common+=1

        sth[(u,v)]=sum+common/(degree[u]+degree[v])  
    return sth

def cal_active_max(fn,currentTime):
    sth={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        max_recent=max(int(x[6]),int(x[7]))       
        sth[(u,v)]=1./(currentTime-max_recent+1)
    return sth    

def cal_active_multi(fn,currentTime,alpha=0.1):
    sth={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
#        multi=math.pow((1-alpha),(currentTime-int(x[6]))) * math.pow((1-alpha),(currentTime-int(x[7])))
        multi=1.0/((currentTime-int(x[6])+1)*(currentTime-int(x[7])+1))      
        sth[(u,v)]=multi
    return sth    

def cal_timespan_to_last(fn,currentTime):
    sth={}
    for line in open(fn):
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])        
        sth[(u,v)]=(float)(int(x[4])/(currentTime-int(x[3])+1))
    return sth

def get_timeList(s):
    timeList=[]    
    sl=s.lstrip('[')
    sr=sl.rstrip(']\n')
    timeList=sr.split(', ')
    return timeList



if __name__=="__main__":

    fn="C:/Users/Administrator/Desktop/Data/missing/test1_time.txt"
    fn_weight="C:/Users/Administrator/Desktop/Data/missing/test11.txt"
    currentTime=1980
    alpha=0.1
    sth=cal_current_last_timespan(fn,currentTime)
    print sth
    sth=cal_current_first_timespan(fn,currentTime)
    print sth
    sth=cal_last_first_timespan(fn)
    print sth
    sth=cal_time_list(fn,currentTime,alpha)
    print sth
    sth=cal_active_max(fn,currentTime)
    print sth
    sth=cal_active_multi(fn,currentTime)
    print sth
    sth=cal_degree_timelist(fn_weight,fn,currentTime,alpha)
    print sth
    sth=cal_jc_timelist(fn_weight, fn, currentTime, alpha)
    print sth
    
    
