# -*- coding: utf-8 -*-
import measure_weight as meas
import preprocess as prep
import statistic as stat
import os
import numpy

def get_sth(f1,time1,measure):
    if measure=="CN":
        sth=meas.cal_CN_weight(f1,time1)
    elif measure=="AA":
        sth=meas.cal_AA_weight(f1,time1)
    elif measure=="PA":
        sth=meas.cal_PA_weight(f1,time1)
    elif measure=="JC":
        sth=meas.cal_JC_weight(f1,time1)
    elif measure=="RA":
        sth=meas.cal_RA_weight(f1,time1)
    elif measure=="DegreeRatio":
        sth=meas.cal_degree_ratio_weight(f1,time1)
    elif measure=="weight":
        sth=meas.cal_weight(f1,time1)
    elif measure=="PA_extend":
        sth=meas.cal_PA_weight_extend(f1,time1)
    
    else:
        print "No such measure!!"
        return
    return sth

def evalute_n(path,interval,output):
    L=[4834 ,5001 ,6357 ,7821 ,8502 ,11233 ,12248 ,16052 ,18686 ,24172 ,28355 ,32340 ,44627 ,49261 ,58994 ,60892 ,89449 ,87920]
    fout = open(output,'w')
    measure=["weight"]
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]
        for year in range(1980, 2000-interval-5, interval):
            fn = [path + str(year+interval*i) + '-' + str(year + interval*(i+1)-1) + 'weight.txt' for i in range(6)]
            sth = meas.cal_w(fn[:-1])
            auc = stat.cal_auc(fn[4],fn[5],sth)
            precision,recall,F1= stat.cal_precision_recall(fn[4],fn[5],sth,L[(year-1981)/interval+4])
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

def evalute_m(path,interval,output):
    L=[4834 ,5001 ,6357 ,7821 ,8502 ,11233 ,12248 ,16052]
    measure=["weight"]
    fout = open(output,'w')
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]
        for year in range(1981, 1990-interval-1, interval):
            f1 = path + str(year) + '-' + str(year + interval-1) + 'weight.txt'
            f2 = path + str(year + interval) + '-' + str(year + interval*2-1) + 'weight.txt'
            sth = get_sth(f1,f1,m)
            auc = stat.cal_auc(f1,f2,sth)
            precision,recall,F1= stat.cal_precision_recall(f1,f2,sth,L[(year-1981)/interval])
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

def evalute_measure(path,interval,output):
    L=[695 ,2168 ,5703 ,16269 ,48820 ,111855 ,311045 ,607057]
    measure=["PA","JC","DegreeRatio","weight","PA_extend","AA","RA","CN"]
    fout = open(output,'w')
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]
        for year in range(1971, 2015-interval-1, interval):
            f1 = path + str(year) + '-' + str(year + interval-1) + 'weight.txt'
            time1 = path + str(year) + '-' + str(year + interval*2-1) + '-commont1.txt'
            time2 = path + str(year) + '-' + str(year + interval*2-1) + '-commont2.txt'
            if year + interval*2-1 > 2014:
                time1 = path + str(year) + '-2014-commont1.txt'
                time2 = path + str(year) + '-2014-commont2.txt'
            sth = get_sth(f1,time1,m)
            auc = stat.cal_auc(time1,time2,sth)
            precision,recall,F1= stat.cal_precision_recall(time1,time2,sth,0.1)
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

def evalute_measure_imdb(path,interval,output):
    L=[247943 ,250335 ,284934 ,335404 ,362603 ,436756]
    measure=["PA","JC","DegreeRatio","weight","PA_extend","AA","RA","CN"]
    fout = open(output,'w')
    for m in measure:
        print m
        PrecisionArr=[]
        RecallArr=[]
        F1Arr=[]
        AUCArr=[]
        for year in range(1990, 1997-interval-1, interval):
            f1 = path + str(year) + '-' + str(year + interval-1) + 'weight.txt'
            time1 = path + str(year) + '-' + str(year + interval*2-1) + '-commont1.txt'
            time2 = path + str(year) + '-' + str(year + interval*2-1) + '-commont2.txt'
            print 1
            sth = get_sth(f1,time1,m)
            print 2
            auc = stat.cal_auc(time1,time2,sth)
            print 3
            precision,recall,F1= stat.cal_precision_recall(time1,time2,sth,0.1)
            print 4
            AUCArr.append(auc)
            PrecisionArr.append(precision)
            RecallArr.append(recall)
            F1Arr.append(F1)
            print f1

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
    '''path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp5/'
    evalute_measure(path,5,path+'result2.txt')'''

    '''path = 'D:\imdb_b\imdb1/'
    evalute_measure_imdb(path,1,path+'result2.txt')'''

    path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp1/'
    evalute_n(path,1,path+'result2.txt')