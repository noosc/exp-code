# -*- coding: utf-8 -*-
import math
import measure
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

def get_interact_timelist(fn):
	interact_list={}
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del reply_nodes
	del all_nodes
	for x in send_nodes:
		interact_list[x]={}
	for line in open(fn):
		x=str(line).split('\t')
		u=int(x[0])
		v=int(x[1])
		t=int(x[2])
		if interact_list[u].has_key(v)==False:
			interact_list[u][v]=[]		
		interact_list[u][v].append(t)
	return interact_list

def get_reply_timelist(fn):
	reply_list={}
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del send_nodes
	del all_nodes
	for x in reply_nodes:
		reply_list[x]={}
	for line in open(fn):
		x=str(line).split('\t')
		u=int(x[0])
		v=int(x[1])
		t=int(x[2])
		if reply_list[v].has_key(u)==False:
			reply_list[v][u]=[]
		reply_list[v][u].append(t)
	return reply_list	

def get_first_time(interact_list_u_v):
	if len(interact_list_u_v)==1:
		return interact_list_u_v[0]
	else:
		min=interact_list_u_v[0]
		for i in interact_list_u_v:
			if i<min:
				min=i 
		return min 

def get_last_time(interact_list_u_v):
	if len(interact_list_u_v)==1:
		return interact_list_u_v[0]
	else:
		max=interact_list_u_v[0]
		for i in interact_list_u_v:
			if i>max:
				max=i 
		return max 

#1
def cal_first_send(fn,currentTime):
	interact_list=get_interact_timelist(fn)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		first=get_first_time(interact_list[u][v])
		sth[edge]=1./(currentTime-first+1)
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#2
def cal_last_send(fn,currentTime):
	interact_list=get_interact_timelist(fn)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		last=get_last_time(interact_list[u][v])
		sth[edge]=1./(currentTime-last+1)
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#3
def cal_send_list(fn,currentTime,alpha):
	interact_list=get_interact_timelist(fn) 
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		sum=0.
		for t in interact_list[u][v]:
			sum+=math.pow((1-alpha),(currentTime-t))
		sth[edge]=sum
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#last send time of node
def get_active(fn):
	active={}
	interact_list=get_interact_timelist(fn)
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del send_nodes
	del reply_nodes
	for node in all_nodes:
		if interact_list.has_key(node):
			last=0
			for i in interact_list[node]:
				for j in interact_list[node][i]:
					if j>last:
						last=j
		else:
			last=0  #注意区分这种情况，节点从未send过
		active[node]=last
	return active

#4
def cal_node_active(fn,currentTime):
	node_active=get_active(fn)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		if node_active[u]==0:
			sth[edge]=0
		else:
			sth[edge]=1./(currentTime-node_active[u]+1)
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

def get_popular(fn):
	popular={}
	reply_list=get_reply_timelist(fn)
	send_nodes,reply_nodes,all_nodes=get_nodes(fn)
	del send_nodes
	del reply_nodes
	for node in all_nodes:
		if reply_list.has_key(node):
			last=0
			for i in reply_list[node]:
				for j in reply_list[node][i]:
					if j>last:
						last=j
		else:
			last=0  #注意区分这种情况，节点从未send过
		popular[node]=last
	return popular

#5
#the time of last received message
def cal_node_popular(fn,currentTime):
	node_popular=get_popular(fn)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		if node_popular[u]==0:
			sth[edge]=0
		else:
			sth[edge]=1./(currentTime-node_popular[u]+1)
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#6
def cal_first_add_last_send(fn,currentTime):
	first_sth=cal_first_send(fn,currentTime)
	last_sth=cal_last_send(fn,currentTime)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		sth[edge]=float(first_sth[edge]+last_sth[edge])/2
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg	

#7
def cal_first_reply(fn,currentTime):
	reply_list=get_reply_timelist(fn)
	sth={}
	edges=get_edges(fn)
	for edge in edges:
		u=edge[0]
		v=edge[1]
		if reply_list.has_key(v) and reply_list[v].has_key(u):
			first=get_first_time(reply_list[v][u])	
			sth[edge]=1./(currentTime-first+1)		
		else:
			sth[edge]=0		
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#8
def cal_last_reply(fn,currentTime):
	reply_list=get_reply_timelist(fn)
	sth={}
	edges=get_edges(fn)
	for edge in edges:
		u=edge[0]
		v=edge[1]
		if reply_list.has_key(v) and reply_list[v].has_key(u):
			last=get_last_time(reply_list[v][u])
			sth[edge]=1./(currentTime-last+1)
		else:
			sth[edge]=0
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

#9
def cal_first_add_last_reply(fn,currentTime):
	first_sth=cal_first_reply(fn,currentTime)
	last_sth=cal_last_reply(fn,currentTime)
	edges=get_edges(fn)
	sth={}
	for edge in edges:
		u=edge[0]
		v=edge[1]
		sth[edge]=float(first_sth[edge]+last_sth[edge])/2
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg

def cal_PA_timelist(fn,currentTime,alpha):
	sth={}
	edges=get_edges(fn)
	interact_list=get_interact_timelist(fn)
	sth1=measure.cal_PA_indegree(fn)
	for edge in edges:
		u=edge[0]
		v=edge[1]
		sum=0.
		for t in interact_list[u][v]:
			sum+=math.pow((1-alpha),(currentTime-int(t)))
		sth[edge]=sum*sth1[edge]
	sth_avg=get_sth_avg(fn,sth)
	return sth_avg



def get_sth_avg(fn,sth):
	edges=get_edges(fn)
	sth_avg={}
	for edge in edges:
		if sth.has_key((edge[1],edge[0])):
			sth_avg[edge]=float(sth[edge]+sth[(edge[1],edge[0])])/2
		else:
			sth_avg[edge]=float(sth[edge])/2
	return sth_avg

if __name__ == '__main__':
	fn="C:/Users/Administrator/Desktop/Data/missing/facebooktest_time1.txt"
	interact_list=get_interact_timelist(fn)
	print interact_list 
	sth=cal_send_list(fn,2015,0.5)
	print sth


