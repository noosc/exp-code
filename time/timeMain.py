# -*- coding: utf-8 -*-
import statistic as stat
import timemeasure2
import evaluate as eva
import os
import numpy


def get_sth2(time1,time2,measure,T,alpha):
    if measure=="cal_first_send":
        sth=timemeasure2.cal_first_send(time1,T)
    elif measure=="cal_last_send":
        sth=timemeasure2.cal_last_send(time1,T)
    elif measure=="cal_send_list":
        sth=timemeasure2.cal_send_list(time1,T,alpha)
    elif measure=="cal_node_active":
        sth=timemeasure2.cal_node_active(time1,T)
    elif measure=="cal_node_popular":
        sth=timemeasure2.cal_node_popular(time1,T)
    elif measure=="cal_first_add_last_send":
        sth=timemeasure2.cal_first_add_last_send(time1,T)
    elif measure=="cal_first_reply":
        sth=timemeasure2.cal_first_reply(time1,T)
    elif measure=="cal_last_reply":
        sth=timemeasure2.cal_last_reply(time1,T)
    elif measure=="cal_first_add_last_reply":
        sth=timemeasure2.cal_first_add_last_reply(time1,T)
    elif measure=="cal_PA_timelist":
        sth=timemeasure2.cal_PA_timelist(time1,T,alpha)
    # elif measure=="cal_common_followee":
    #     sth=M.cal_common_followee(time1)
    # elif measure=="cal_PA_indegree":
    #     sth=M.cal_PA_indegree(time1) 
    # elif measure=="cal_PA_outdegree":
    #     sth=M.cal_PA_outdegree(time1) 
    # elif measure=="cal_PA_inoutdegree":
    #     sth=M.cal_PA_inoutdegree(time1)
    # elif measure=="cal_PA_follower":
    #     sth=M.cal_PA_follower(time1) 
    # elif measure=="cal_PA_followee":
    #     sth=M.cal_PA_followee(time1) 
    # elif measure=="cal_PA_follower_followee":
    #     sth=M.cal_PA_follower_followee(time1) 
                     
    else:
        print "No such mesure!!"
    return sth

def evalute_measure_fb(path,interval,output):
    L = [12118 ,15930 ,19422 ,18195 ,18529 ,23451 ,32751, 37504]
    currentTime=[20070401,20070701,20071001,20080101,20080401,20080701,20081001,20090101]
    alpha=[0.1,0.2,0.3,0.4]
    measure=["cal_send_list","cal_PA_timelist"]
    #measure=["last","first","timespan","timelist","activeMax","activeMulti","timespan_to_last","degree_timelist","cal_jc_timelist"]
    fout = open(output,'w')
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]

        if m=="cal_send_list" or m=="cal_PA_timelist":
            for i in range(len(alpha)):
                print alpha[i]
                PrecisionArr=[]
                RecallArr=[]
                F1Arr=[]
                AUCArr=[]
                for months in range(2007*12, 2009*12, interval):
                    time1 = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1) + '.txt'
                    next = months+interval
                    time2 = path + str(next/12*100+next%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1) + '.txt'
                    sth = get_sth2(time1,time2,m,currentTime[(months-2007*12)/interval],alpha[i])
                    auc = eva.cal_auc(time1,time2,sth)
                    precision,recall,F1= eva.cal_precision_recall(time1,time2,sth,L[(months-2007*12)/interval])
                    AUCArr.append(auc)
                    PrecisionArr.append(precision)
                    RecallArr.append(recall)
                    F1Arr.append(F1)
                fout.write(m + '\t' + str(alpha[i]) + '\n')
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
        else:
            for months in range(2007*12, 2009*12, interval):
                time1 = path + str(months/12*100+months%12+1) + '-' + str((months+interval-1)/12*100+(months+interval-1)%12+1) + '.txt'
                next = months+interval
                time2 = path + str(next/12*100+next%12+1) + '-' + str((next+interval-1)/12*100+(next+interval-1)%12+1) + '.txt'
                sth = get_sth2(time1,time2,m,currentTime[(months-2007*12)/interval],alpha[0])
                auc = eva.cal_auc(time1,time2,sth)
                AUCArr.append(auc)
                precision,recall,F1= eva.cal_precision_recall(time1,time2,sth,L[(months-2007*12)/interval])
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
    evalute_measure_fb(path,3,path + 'result3.txt')
#     time1='C:/Users/Administrator/Desktop/data/missing/dblp_time_common/1/1970-1980-common.txt'
#     time2='C:/Users/Administrator/Desktop/data/missing/dblp_time_common/1/1980-1985-common.txt'
#     fn_weight='C:/Users/Administrator/Desktop/data/missing/dblp_weight/1970-1980.txt'
#     currentTime=1980
#     L=2000
#     stat.cal_miss_ratio(time1,time2)
# #    measure=["last","first","timespan","activeMax","activeMulti","timelist"]
#     measure=["cal_jc_timelist"]
#     for m in measure:
#         if m=="cal_jc_timelist":
#             print m
#             for alpha in range(5,7):
#                 sth=get_sth(fn_weight,time1,currentTime,alpha*0.1,m) 
#                 print alpha*0.1
#                 stat.cal_auc(time1,time2,sth)
#                 stat.test_prf(time1,time2,sth,L)

#                 print
#         else:
#             sth=get_sth(fn_weight,time1,currentTime,0.5,m)
#             print m
#             stat.cal_auc(time1,time2,sth)
#             stat.cal_precision_recall(time1,time2,sth,L)
#             stat.test_prf(time1,time2,sth,L)
#             print
    
