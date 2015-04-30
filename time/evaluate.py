# -*- coding: utf-8 -*-
from sklearn.metrics import classification_report,auc_score,auc

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

#该miss算的是：一条连接u——v当如下两种情况都不存在时，才算消失。1.u——v 2.v-u
def cal_miss_ratio(fn1,fn2):
	edges_1=read_edges(fn1)
	edges_2=read_edges(fn2)
    
	print "edges_1 "+str(len(edges_1))
	print "edges_2 "+str(len(edges_2))
    
	miss_num=0
	for edge1 in edges_1:
		bedge=(edge1[1],edge1[0])
		if (edge1 not in edges_2) and (bedge not in edges_2):
			miss_num+=1
	miss_ratio=float(miss_num)/len(edges_1)
	print "miss_ratio is "+str(miss_ratio)

#该miss算的是：一条连接u——v只要time2中不存在u——v即为消失
def cal_miss_ratio2(fn1,fn2):
	edges_1=read_edges(fn1)
	edges_2=read_edges(fn2)
    
	print "edges_1 "+str(len(edges_1))
	print "edges_2 "+str(len(edges_2))
    
	miss_ratio=float(len(edges_1-edges_2))/len(edges_1)

	print "miss_ratio is "+str(miss_ratio)

def cal_precision_recall(fn1,fn2,sth,L):
	edges_1=read_edges(fn1)
	edges_2=read_edges(fn2)
#	missing 2
#	edges_miss=edges_1-edges_2
#   missing 1
	edges_miss=set()
	for edge1 in edges_1:
		bedge=(edge1[1],edge1[0])
		if (edge1 not in edges_2) and (bedge not in edges_2):
			edges_miss.add(edge1)
#	print edges_miss

	predict_set={}
	for key in sth.keys():
		predict_set[key]=predict_set.get(key,0.)+sth[key]
	predict_set=sorted(predict_set.iteritems(),key=lambda d:d[1],reverse=False)#

    ##record the first L edges whose strength is weak. 
	predict_L=set()
	for i in range(L):
		predict_L.add(predict_set[i][0])

#	print predict_L    
	precision=float(len(predict_L & edges_miss))/len(predict_L)
	recall=float(len(predict_L & edges_miss))/len(edges_miss)
	if (precision+recall)!=0:
		F1=2*(precision*recall)/(precision+recall)
	else:
		F1=0
	#print "The precision is "+str(precision)
	#print "The recall is "+str(recall)
	#print "The F1 is "+str(F1)
	return precision,recall,F1

def cal_auc(fn1,fn2,sth):
	edges_1=read_edges(fn1)
	edges_2=read_edges(fn2)
#	missing 2
#	edges_miss=edges_1-edges_2
#   missing 1
	edges_miss=set()
	for edge1 in edges_1:
		bedge=(edge1[1],edge1[0])
		if (edge1 not in edges_2) and (bedge not in edges_2):
			edges_miss.add(edge1)

	pos=len(edges_miss)
	neg=len(edges_1)-pos
	print pos,neg
	predict_set={}
	for key in sth.keys():
		predict_set[key]=predict_set.get(key,0.)+sth[key]
	predict_set=sorted(predict_set.iteritems(),key=lambda d:d[1],reverse=False)##predict_set is list

	xy_arr=[]
	tp, fp = 0., 0.
    
	for i in range(len(predict_set)):
		if (predict_set[i][0] in edges_miss):
			tp+=1
		else:
			fp+=1
		xy_arr.append([fp/neg,tp/pos])
    
	auc=0.
	prev_x=0
	for x,y in xy_arr:
		if x!=prev_x:
			auc+=(x-prev_x)*y
			prev_x=x

	print "auc is "+str(auc)  
	return auc 

if __name__=='__main__':
	time1="C:/Users/Administrator/Desktop/Data/missing/facebooktest_time1.txt"
	time2="C:/Users/Administrator/Desktop/Data/missing/facebooktest_time2.txt"
	sth={(1,2):1,(2,1):0.5,(3,1):1.0,(4,1):1,(2,6):0.5,(6,2):1,(5,2):0.75,(5,1):0.25}
	cal_miss_ratio(time1,time2)
	cal_precision_recall(time1,time2,sth,2)
#	test_prf(time1,time2,sth,2)
	cal_auc(time1,time2,sth)