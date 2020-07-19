# _*_ coding: UTF-8 _*_

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
import sklearn.neighbors as sn
from scipy.cluster import hierarchy
from sklearn import decomposition as skldec
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from app.util.plt.catagory_analyze import hierarchyDendrogram, pltACP, pltKmeans, pltDbscan

#贝叶斯分类
def def_GNB(X1, y1):
    GNB = GaussianNB()
    #有bug
    GNB.fit(X1, y1)
    pred = GNB.predict(X1)

    l1 = list(pred)
    dict1 = {}
    for i in range(len(l1)):
        if l1[i] in dict1.keys():
            dict1[l1[i]] += 1
        else:
            dict1[l1[i]] = 1
    l = list(y1 == pred)
    dict = {}
    for i in range(len(l)):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1
    if len(dict.keys()) == 1:
        if True in dict.keys():
            dict[False] = 0
        else:
            dict[True] = 0
    dict['正确率'] = dict[True] / (dict[True] + dict[False])

    return pred, dict, dict1

#KNN分类
def def_KNN(X1, y1, n, weights1='distance'):
    model = sn.KNeighborsClassifier(n_neighbors=n, weights=weights1)
    #报bug
    model.fit(X=X1, y=y1)
    pred = model.predict(X1)

    l1 = list(pred)
    dict1 = {}
    for i in range(len(l1)):
        if l1[i] in dict1.keys():
            dict1[l1[i]] += 1
        else:
            dict1[l1[i]] = 1
    l = list(y1 == pred)
    dict = {}
    for i in range(len(l)):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1
    if len(dict.keys()) == 1:
        if True in dict.keys():
            dict[False] = 0
        else:
            dict[True] = 0

    dict['正确率'] = dict[True] / (dict[True] + dict[False])

    return pred, dict, dict1

#线性判别
def def_fisher(X1, y1):
    LDA = LinearDiscriminantAnalysis()
    #报bug
    LDA.fit(X=X1, y=y1)
    pred = LDA.predict(X1)

    l1 = list(pred)
    dict1 = {}
    for i in range(len(l1)):
        if l1[i] in dict1.keys():
            dict1[l1[i]] += 1
        else:
            dict1[l1[i]] = 1
    l = list(y1 == pred)
    dict = {}
    for i in range(len(l)):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1
    if len(dict.keys()) == 1:
        if True in dict.keys():
            dict[False] = 0
        else:
            dict[True] = 0
    dict['正确率'] = dict[True] / (dict[True] + dict[False])

    return pred, dict, dict1

#######################################################################################################################

#系统聚类（传入数据，类别个数，判断方法，）
def def_hierarchy(X, n_clusters1=3, method1='complete', metric1='euclidean', n_components1=0.95):
    #构建聚类器
    model = hierarchy.linkage(X, method=method1, metric=metric1)

    #取得绘图的路径
    file_path1,label = hierarchyDendrogram(X,model,n_clusters1)
    file_path2 = pltACP(X,n_components1,label)

    l = list(label)
    dict = {}
    for i in range(len(l)):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1

    return label, file_path1, file_path2, dict

#kmeans聚类
def def_kmeans(X, n_clusters1=3, n_components1=0.95):
    model = KMeans(n_clusters=n_clusters1, init='k-means++', n_init=n_clusters1)
    model.fit(X)
    centers = model.cluster_centers_
    labels = model.labels_

    pca = skldec.PCA(n_components=n_components1)
    pca.fit(X)
    result = pca.transform(X)

    #取得绘图的路径
    file_path = pltKmeans(result,labels,pca)

    l = list(labels)
    dict = {}
    for i in range(len(l)):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1

    return centers, labels, file_path, dict

#DBSCAN聚类
def def_DBSCAN(X, eps1=0.5, min_samples1=5, n_components1=0.95):
    model = DBSCAN(eps=eps1, min_samples=min_samples1)
    model.fit(X)

    core_samples_mask = np.zeros_like(model.labels_, dtype=bool)
    core_samples_mask[model.core_sample_indices_] = True

    labels = model.labels_
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)

    pca = skldec.PCA(n_components=n_components1)
    pca.fit(X)
    result = pca.transform(X)

    #返回绘图路径
    file_path = pltDbscan(result, labels, pca)

    l = list(labels)
    dict = {}
    a = len(l)
    for i in range(a):
        if l[i] in dict.keys():
            dict[l[i]] += 1
        else:
            dict[l[i]] = 1

    return labels, file_path, dict
