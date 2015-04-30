import numpy as np
import sklearn
import generateFeature
import math
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import svm
from sklearn import naive_bayes
from sklearn import tree
from sklearn import ensemble
from sklearn import neighbors
from sklearn import cluster
from sklearn import metrics
from sklearn.feature_selection import RFE
from sklearn.decomposition import PCA
from sklearn.semi_supervised import label_propagation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report

def file2matrix(filename):
    arr=np.loadtxt(filename,delimiter='\t')
    arrayOfFeature=arr[:,2:-1]
    arrayOfLabel=arr[:,-1]

    #normalized_Feature=preprocessing.normalize(arrayOfFeature)
    stardardized_Feature=preprocessing.scale(arrayOfFeature)

    return stardardized_Feature,arrayOfLabel

# fit an AdaBoost classifier with n_estimators weak learners
def GradientBoost(file1,file2):
    feature1,lable1=file2matrix(file1)

    clf=ensemble.GradientBoostingClassifier()
    clf.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred


# Naive bayes
def NB(file1,file2):
    feature1,lable1=file2matrix(file1)

    # pca = PCA(n_components=15)
    # pca.fit(feature1)
    # feature_reduce=pca.transform(feature1)

    gnb=naive_bayes.GaussianNB()
    gnb.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)

    # pca = PCA(n_components=15)
    # pca.fit(feature2)
    # feature_reduce2=pca.transform(feature2)

    y_true=label2
    y_score=y_pred = gnb.predict(feature2)
    return y_true,y_score,y_pred

#Stochastic Gradient Descent
#loss="hinge": (soft-margin) linear Support Vector Machine, 
#loss="modified_huber": smoothed hinge loss,
#loss="log": Logistic Regression,
def SGDclf(file1,file2):
    feature1,lable1=file2matrix(file1)
    clf=linear_model.SGDClassifier(loss="log", penalty="l2")
    clf.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred

#Unbalanced problems:  implement a keyword class_weight in the fit method
def SVM(file1,file2):
    feature1,lable1=file2matrix(file1)
    clf=svm.SVC(C= 5, gamma = 1.0/20000)
    #para = {'kernel': ('linear','rbf'), 'C' : [1,8]}
    #clf = GridSearchCV(svr, para)
    clf.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred

# Ordinary Least Squares
def LinearReg(file1,file2):
    feature1,lable1=file2matrix(file1)
    regr=LinearRegression()
    regr.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=regr.decision_function(feature2)
    y_pred = regr.predict(feature2)
    return y_true,y_score,y_pred

#Ridge regression addresses some of the problems
# of Ordinary Least Squares by imposing a penalty on the size of coefficients.
def RidgeReg(file1,file2):
    feature1,lable1=file2matrix(file1)
    clf=RidgeClassifier()
    clf.fit(feature1,lable1)

    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred

def LassoReg(file1,file2):
    feature1,lable1=file2matrix(file1)
    reg=linear_model.Lasso()
    reg.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=reg.decision_function(feature2)
    y_pred = reg.predict(feature2)
    return y_true,y_score,y_pred

def BayesianReg(file1,file2):
    feature1,lable1=file2matrix(file1)
    reg=linear_model.BayesianRidge()
    reg.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=reg.decision_function(feature2)
    y_pred = reg.predict(feature2)
    return y_true,y_score,y_pred

def LogisticReg(file1,file2):
    feature1,lable1=file2matrix(file1)
    reg=linear_model.LogisticRegression(penalty='l1',tol=0.01)
    reg.fit(feature1,lable1)

    feature2,label2=file2matrix(file2)
    y_true=label2
    y_pred=reg.predict(feature2)
    y_score=reg.decision_function(feature2)

    return y_true,y_score,y_pred

def KNN(file1,file2):
    feature1,lable1=file2matrix(file1)
    neigh=KNeighborsClassifier(n_neighbors=1,warn_on_equidistant=False,weights="distance")

    neigh.fit(feature1,lable1)

    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=neigh.decision_function(feature2)
    y_pred = neigh.predict(feature2)
    return y_true,y_score,y_pred

def RandomForest(file1,file2):
    feature1,lable1=file2matrix(file1)
    clf=ensemble.RandomForestClassifier(n_estimators=10)
    clf.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred

def DTree(file1,file2):
    feature1,lable1=file2matrix(file1)
    clf=tree.DecisionTreeClassifier()
    clf.fit(feature1,lable1)
    feature2,label2=file2matrix(file2)
    y_true=label2
    y_score=clf.decision_function(feature2)
    y_pred = clf.predict(feature2)
    return y_true,y_score,y_pred

     
def ClassifierTest(file1,file2,output):
    fout = open(output,'w')
    m = ['GradientBoost','NB','SGDclf','SVM','LogisticReg']
    #m = ['GradientBoost','NB','SGDclf','SVM','LinearReg','RidgeReg','LassoReg','BayesianReg','LogisticReg','KNN','RandomForest','DTree']
    for f in m:
        if f == 'GradientBoost':
           y_true,y_score,y_pred=GradientBoost(file1, file2)
        elif f == 'NB':
           y_true,y_score,y_pred=NB(file1, file2)
        elif f == 'SGDclf':
           y_true,y_score,y_pred=SGDclf(file1, file2)
        elif f == 'SVM':
           y_true,y_score,y_pred=SVM(file1, file2)
        elif f == 'LinearReg':
           y_true,y_score,y_pred=LinearReg(file1, file2)
        elif f == 'RidgeReg':
           y_true,y_score,y_pred=RidgeReg(file1, file2)
        elif f == 'LassoReg':
           y_true,y_score,y_pred=LassoReg(file1, file2)
        elif f == 'BayesianReg':
           y_true,y_score,y_pred=BayesianReg(file1, file2)
        elif f == 'LogisticReg':
           y_true,y_score,y_pred=LogisticReg(file1, file2)
        elif f == 'KNN':
           y_true,y_score,y_pred=KNN(file1, file2)
        elif f == 'RandomForest':
           y_true,y_score,y_pred=RandomForest(file1, file2)
        elif f == 'DTree':
           y_true,y_score,y_pred=DTree(file1, file2)
        print f
    #    print classification_report(y_true,y_score)
    #    print metrics.confusion_matrix(y_true,y_score)
        #accuracy=sklearn.metrics.accuracy_score(y_true,y_pred)
        precision=sklearn.metrics.precision_score(y_true,y_pred)
        recall=sklearn.metrics.recall_score(y_true,y_pred)
        auc=sklearn.metrics.roc_auc_score(y_true,y_score)
    #    auc2=sklearn.metrics.auc(y_true, y_score)
        fout.write(f+':\n')
        fout.write('precision: '+str(precision)+' recall: '+str(recall) + '\n')
        fout.write('auc: '+str(auc) + '\n\n')
#    print('auc: '+str(auc2))
    fout.close()


def cal_auc(y_true,y_score):
    length=len(y_score)
    print length
    i=0
    j=length-1
    while(i<j):
        while(i<j & (math.fabs(y_score[i]-0.)<0.01)):
            i=i+1
        while(i<j & (math.fabs(y_score[j]-1.)<0.01)):
            j=j-1
        if(i<j):
            temp=y_score[i]
            y_score[i]=y_score[j]
            y_score[j]=temp

            tmp=y_true[i]
            y_true[i]=y_true[j]
            y_true[j]=tmp

    print length
    xy_arr=[]
    tp=0.
    fp=0.
    pos=0
    neg=0
    for k in range(length):
        if y_true[k]==0:
            pos+=1
        else:
            neg+=1
    print pos
    print neg

    for k in range(length):
        if(y_true[k]==0):
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

if __name__ == '__main__':
    #file1='C:/Users/Administrator/Desktop/data/missing/out/testout1.txt'
    #file2='C:/Users/Administrator/Desktop/data/missing/out/testout2.txt'
    #file1='C:/Users/Administrator/Desktop/data/missing/dblp_feature_common/1/1970-1980-common.txt'
    #file2='C:/Users/Administrator/Desktop/data/missing/dblp_feature_common/1/1980-1985-common.txt'
    #file3='C:/Users/Administrator/Desktop/data/missing/dblp_feature_common/1/1985-1990-common.txt'
    '''path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp5/'
    interval = 5
    for year in range(1971, 2005-interval*2-1, interval):
        fn1 = path + str(year) + '-' + str(year + interval-1) + '-flc1.txt'
        fn2 = path + str(year + interval) + '-' + str(year + interval*2-1) + '-flc2.txt'
        ClassifierTest(fn1,fn2,'KNN',path+'result4.txt')
    ClassifierTest(path+'1981-1985-flc1.txt',path+'1986-1990-flc2.txt',path+'result4.txt')'''

    path = 'C:\Users\cc\Desktop\dblp_coauthor\dblp_coauthor/dblp1/'
    ClassifierTest(path+'1985-1985-fl.txt',path+'1986-1986-fl.txt',path+'result4.txt')





