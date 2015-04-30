# -*- coding: utf-8 -*-

def get_nodes(fn):
    f=open(fn)
    send_nodes=set()
    reply_nodes=set()
    all_nodes=set()

    for line in f:
        x=str(line).split('\t')
        u=int(x[0])
        v=int(x[1])
        send_nodes.add(u)
        reply_nodes.add(v)
        all_nodes.add(u)
        all_nodes.add(v)
    f.close()
    return send_nodes,reply_nodes,all_nodes

def get_edges(fn):
	edges=set()
	for line in open(fn):
		x=str(line).split('\t')
		u=int(x[0])
		v=int(x[1])
		edges.add((u,v))
	return edges		

def get_interact(fn):
	interact={}
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del reply_nodes
	del all_nodes
	for x in send_nodes:
		interact[x]={}
	for line in open(fn):
		x=str(line).split('\t')
		u=int(x[0])
		v=int(x[1])
		if interact[u].has_key(v)==False:
			interact[u][v]=0
		interact[u][v]+=1
#	print interact
	return interact

def get_indegree_outdegree(fn):
	outdegree={}
	indegree={}
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del all_nodes
	interact=get_interact(fn)

	for x in reply_nodes:   ##init
		indegree[x]=0
	for x in send_nodes:
		outdegree[x]=0
	for x in send_nodes:
		for y in interact[x]:
			outdegree[x]+=interact[x][y]
			indegree[y]+=interact[x][y]
	return indegree,outdegree

def get_follower_followee(fn):
	follower={} ##in
	followee={} ##out
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del all_nodes
	interact=get_interact(fn)
	for x in send_nodes:   ##init
		followee[x]=set()
	for x in reply_nodes:   ##init
		follower[x]=set()
	for x in send_nodes:
		for y in interact[x]:
			followee[x].add(y)
			follower[y].add(x)
	return follower,followee

#1
def cal_send_times(fn):
	sth={}
	edges=get_edges(fn)
	interact=get_interact(fn)
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		sth[edge]=interact[u][v]
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#2
def cal_reply_times(fn):
	sth={}
	edges=get_edges(fn)
	interact=get_interact(fn)
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if interact.has_key(v) and interact[v].has_key(u):		
			sth[edge]=interact[v][u]
		else:
			sth[edge]=0
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg	

#3
def cal_send_AND_reply(fn):
	sth={}
	edges=get_edges(fn)
	interact=get_interact(fn)
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if interact.has_key(v) and interact[v].has_key(u):
			sth[edge]=interact[u][v]+interact[v][u]
		else:
			sth[edge]=interact[u][v]		
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg	

#4
def cal_send_ratio(fn):
	sth={}
	edges=get_edges(fn)
	interact=get_interact(fn)
	indegree,outdegree=get_indegree_outdegree(fn)
	del indegree
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		sth[edge]=float(interact[u][v])/outdegree[u]
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#5
def cal_follower_B_followee(fn):
	sth={}
	edges=get_edges(fn)
	follower,followee=get_follower_followee(fn)	
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if follower.has_key(u):
			sth[edge]=float(len(follower[u]))/len(followee[u])
		else:
			sth[edge]=0
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#6
def cal_reply_ratio(fn):
	sth={}
	edges=get_edges(fn)
	interact=get_interact(fn)	
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if interact.has_key(v) and interact[v].has_key(u):		
			sth[edge]=float(interact[v][u])/interact[u][v]
		else:
			sth[edge]=0
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#7
def cal_prestige_versus(fn):
	sth={}
	edges=get_edges(fn)
	follower,followee=get_follower_followee(fn)	
	del followee
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if follower.has_key(u):
			small=min(len(follower[u]),len(follower[v]))
			big=max(len(follower[u]),len(follower[v]))
		else:
			small=0
			big=len(follower[v])
		sth[edge]=float(small)/big
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#8  VS  7
def cal_indegree_versus(fn):
	sth={}
	edges=get_edges(fn)
	indegree,outdegree=get_indegree_outdegree(fn)	
	del outdegree
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if indegree.has_key(u):
			small=min(indegree[u],indegree[v])
			big=max(indegree[u],indegree[v])
		else:
			small=0
			big=indegree[v]
		sth[edge]=float(small)/big
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#9  VS  5
def cal_indegree_B_outdegree(fn):
	sth={}
	edges=get_edges(fn)
	indegree,outdegree=get_indegree_outdegree(fn)	
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if indegree.has_key(u):
			sth[edge]=float(indegree[u])/(outdegree[u])
		else:
			sth[edge]=0
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg 

#10
def cal_indegree_v(fn):
	sth={}
	edges=get_edges(fn)
	indegree,outdegree=get_indegree_outdegree(fn)	
	del outdegree
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		sth[edge]=indegree[v]
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#11
def cal_common_followee(fn):
	sth={}
	edges=get_edges(fn)
	follower,followee=get_follower_followee(fn)	
	del followee
	for edge in edges:
		u=int(edge[0])
		v=int(edge[1])
		if follower.has_key(u):
			common=len(follower[u] & follower[v])
		else:
			common=0
		sth[edge]=common
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

def get_sth_avg(fn,sth):
	edges=get_edges(fn)
	sth_avg={}
	for edge in edges:
		if sth.has_key((edge[1],edge[0])):
			sth_avg[edge]=float(sth[edge]+sth[(edge[1],edge[0])])/2
		else:
			sth_avg[edge]=sth[edge]/2
	return sth_avg

if __name__=="__main__":

    fn="C:/Users/Administrator/Desktop/Data/missing/facebooktest_time1.txt"

    sth=cal_follower_B_followee(fn)
    print sth

#11. cal_common_followee
#10. cal_indegree_v
#9. cal_indegree_B_outdegree
#8. cal_indegree_versus
#7. cal_prestige_versus
#6. cal_reply_ratio
#5. cal_follower_B_followee
#4. cal_send_ratio
#3. cal_send_AND_reply
#2. cal_reply_times
#1. cal_send_times