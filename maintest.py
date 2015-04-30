# -*- coding: utf-8 -*-
import statistic as stat
import preprocess as prep
import weightMeasure as DR
import evaluate as eva
import measure as M
import os
import numpy


def get_sth2(time1,time2,measure):
    if measure=="cal_send_times":
        sth=M.cal_send_times(time1)
    elif measure=="cal_reply_times":
        sth=M.cal_reply_times(time1)
    elif measure=="cal_send_AND_reply":
        sth=M.cal_send_AND_reply(time1)
    elif measure=="cal_send_ratio":
        sth=M.cal_send_ratio(time1)
    elif measure=="cal_follower_B_followee":
        sth=M.cal_follower_B_followee(time1)
    elif measure=="cal_reply_ratio":
        sth=M.cal_reply_ratio(time1)
    elif measure=="cal_prestige_versus":
        sth=M.cal_prestige_versus(time1)
    elif measure=="cal_indegree_versus":
        sth=M.cal_indegree_versus(time1)
    elif measure=="cal_indegree_B_outdegree":
        sth=M.cal_indegree_B_outdegree(time1)
    elif measure=="cal_indegree_v":
        sth=M.cal_indegree_v(time1)
    elif measure=="cal_common_followee":
        sth=M.cal_common_followee(time1)    
    else:
        print "No such mesure!!"
    return sth

def evalute_measure_fb(path,interval,output):
    measure=["cal_send_times","cal_reply_times","cal_send_AND_reply","cal_send_ratio",\
    "cal_follower_B_followee","cal_reply_ratio","cal_prestige_versus",\
    "cal_indegree_versus","cal_indegree_B_outdegree","cal_indegree_v",\
    "cal_common_followee"]
    L = [12118 ,15930 ,19422 ,18195 ,18529 ,23451 ,32751, 37504]
    fout = open(output,'w')
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]
        for months in range(2007*12, 2009*12, interval):
            time1 = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1) + '.txt'
            next = months+interval
            time2 = path + str(next/12*100+next%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1) + '.txt'
            sth = get_sth2(time1,time2,m)       
            precision,recall,F1 = eva.cal_precision_recall(time1,time2,sth,L[(months-2007*12)/interval])
            auc = eva.cal_auc(time1,time2,sth)

            AUCArr.append(auc)
            PrecisionArr.append(precision)
            RecallArr.append(recall)
            F1Arr.append(F1)

        fout.write(m + '\n')
        fout.write("PrecisionArr\n")
        fout.write(str(PrecisionArr) + '\n')
        fout.write(str(numpy.mean(PrecisionArr)) + '\n')
        fout.write("RecallArr\n")
        fout.write(str(RecallArr) + '\n')
        fout.write(str(numpy.mean(RecallArr)) + '\n')
        fout.write("F1Arr\n")
        fout.write(str(F1Arr) + '\n')
        fout.write(str(numpy.mean(F1Arr)) + '\n')
        fout.write("AUCArr\n")
        fout.write(str(AUCArr) + '\n')
        fout.write(str(numpy.mean(AUCArr)) + '\n\n')
    fout.close()

if __name__=='__main__':
    path = 'C:\Users\cc\Desktop/facebook-wall/facebook3/'
    evalute_measure_fb(path,3,path + 'result1.txt')
    
#     time1='C:/Users/Administrator/Desktop/data/missing/dblp3/2/1980-1985-common.txt'
#     time2='C:/Users/Administrator/Desktop/data/missing/dblp3/2/1985-1990-common.txt'
#     f1='C:/Users/Administrator/Desktop/data/missing/dblp4/2/1980-1985-common.txt'
#     stat.cal_miss_ratio(time1,time2)
#     L=4500
#     print
# #    measure=["degree_ratio","embed","clust","CN","AA","RA"]
#     measure=["PA","JC","degree_ratio","embed","clust","AA","RA","CN"]
#     for m in measure:
#         sth=get_sth(f1,time1,m)
#         print m
#         stat.cal_auc(time1,time2,sth)
#         stat.cal_precision_recall(time1,time2,sth,L)
# #        stat.test_prf(time1,time2, sth, L)
#         print
#         # for L in range(1000,6000,1000):
#         #     print "L is "+str(L)+" -------------------"
#         #     stat.cal_precision_recall(time1,time2,sth,L)

    
##    test using the small network
##    time1='C:/Users/Administrator/Desktop/data/missing/time1test.txt'
##    time2='C:/Users/Administrator/Desktop/data/missing/time2.txt'
##    f1='C:/Users/Administrator/Desktop/data/missing/time1.txt'
##    L=4
##    sth=DR.cal_edge_betweenness(f1,time1)
##    stat.cal_precision_recall(time1,time2,sth,L)
##    stat.cal_auc(time1,time2,sth)
