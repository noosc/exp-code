import preprocess as prep
from sklearn.metrics import classification_report,auc_score,auc

def cal_miss_ratio(fn1,fn2):
    edges_1=prep.read_edges(fn1)
    edges_2=prep.read_edges(fn2)
    
    print "edges_1 "+str(len(edges_1))
    print "edges_2 "+str(len(edges_2))
    
    miss_ratio=float(len(edges_1-edges_2))/len(edges_1)
    new_ratio=float(len(edges_2-edges_1))/len(edges_1)

    print "miss_ratio is "+str(miss_ratio)
    print "new added ratio is "+str(new_ratio)

def cal_precision_recall(fn1,fn2,sth,L):
    edges_1=prep.read_edges(fn1)
    edges_2=prep.read_edges(fn2)
    edges_miss=edges_1-edges_2
    
    predict_set={}
    for key in sth.keys():
        predict_set[key]=predict_set.get(key,0.)+sth[key]
    predict_set=sorted(predict_set.iteritems(),key=lambda d:d[1],reverse=False)#

    ##record the first L edges whose strength is weak. 
    predict_L=set()
    for i in range(L):
        predict_L.add(predict_set[i][0])

#    print predict_L    
    precision=float(len(predict_L & edges_miss))/len(predict_L)
    recall=float(len(predict_L & edges_miss))/len(edges_miss)
    F1=2*(precision*recall)/(precision+recall)
    return precision,recall, F1

def test_prf(fn1,fn2,sth,L):
    y_true=[]
    y_score=[]
    edges_1=prep.read_edges(fn1)
    edges_2=prep.read_edges(fn2)
    
    predict_set={}
    for key in sth.keys():
        predict_set[key]=predict_set.get(key,0.)+sth[key]
    predict_set=sorted(predict_set.iteritems(),key=lambda d:d[1],reverse=True)#

    threshold=predict_set[L][1]
    for i in edges_1:
        if sth[i]>threshold:
            y_score.append(1)
        else:
            y_score.append(0)

    for i in edges_1:
        if i not in edges_2:
            y_true.append(0)
        else:
            y_true.append(1)

    print classification_report(y_true,y_score)
    print auc_score(y_true,y_score)
 


def cal_auc(fn1,fn2,sth):
    edges_1=prep.read_edges(fn1)
    edges_2=prep.read_edges(fn2)
    edges_miss=edges_1-edges_2

    pos=len(edges_miss)
    neg=len(edges_1)-pos

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

    return auc  
    
if __name__=='__main__':
    fn1='C:/Users/Administrator/Desktop/data/missing/time1.txt'
    fn2='C:/Users/Administrator/Desktop/data/missing/time2.txt'
    cal_miss_ratio(fn1,fn2)

    sth={(1,2):0.7,(1,3):0.2,(1,6):0.5,(2,5):0.2,
    (2,6):0.3,(3,4):0.2,(4,8):0.2,(4,9):0.5,
    (5,9):0.3,(6,7):0.5,(8,10):0.6,(8,11):0.6,
    (8,12):0.6,(10,11):0.7,(10,12):0.7,(11,12):0.7}
    test_prf(fn1,fn2,sth,6)
    #cal_auc(fn1,fn2,sth)

    

