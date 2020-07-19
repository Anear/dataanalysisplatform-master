# _*_ coding: UTF-8 _*_

from scipy.cluster import hierarchy
import os
import time
import matplotlib.pyplot as plt
from scipy import cluster
from sklearn import decomposition as skldec

def hierarchyDendrogram(X,model,n_clusters1):
    # 绘制层次聚类图
    hierarchy.dendrogram(model, labels=X.index)

    # 保存到本地
    file_name = 'hierarchy' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    plt.close()
    file_path1 = '\\static\\PythonPlot\\' + file_name
    label = cluster.hierarchy.cut_tree(model, n_clusters=n_clusters1)
    label = label.reshape(label.size, )
    return file_path1,label

def pltACP(X,n_components1,label):
    #利用PCA函数绘制散点图，主成分分析
    # 选择方差95%的占比
    pca = skldec.PCA(n_components = n_components1)
    #主成分分析时每一行是一个输入数据，数据拟合
    pca.fit(X)
    #报bug
    # 计算结果
    result = pca.transform(X)
    # 绘制图形显示结果
    plt.figure()
    # 绘制两个主成分组成坐标的散点图
    plt.scatter(result[:, 0], result[:, 1], c=label, edgecolor='k')
    #  在每个点边上绘制数据名称
    for i in range(result[:0].size):
        plt.text(result[i, 0], result[i, 1], X.index[i])
    # x轴标签字符串
    x_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[0] * 100), 2)
    # y轴标签字符串
    y_label = 'PC2(%s%%)' % round((pca.explained_variance_ratio_[1] * 100), 2)
    # 绘制x轴标签
    plt.xlabel(x_label)
    # 绘制y轴标签
    plt.ylabel(y_label)

    #保存到本地
    file_name2 = 'hierarchy2' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name2)
    plt.close()
    file_path2 = '\\static\\PythonPlot\\' + file_name2

    return file_path2


def pltKmeans(result, labels, pca):
    plt.figure()
    plt.scatter(result[:, 0], result[:, 1], c=labels, edgecolor='k')
    for i in range(result[:0].size):
        plt.text(result[i, 0], result[i, 1], X.index[i])
    x_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[0] * 100), 2)
    y_label = 'PC2(%s%%)' % round((pca.explained_variance_ratio_[1] * 100), 2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    file_name = 'kmeans' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    plt.close()

    file_path = '\\static\\PythonPlot\\' + file_name

    return file_path

def pltDbscan(result, labels, pca):
    plt.figure()
    plt.scatter(result[:, 0], result[:, 1], c=labels, edgecolor='k')
    for i in range(result[:0].size):
        plt.text(result[i, 0], result[i, 1], X.index[i])
    x_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[0] * 100), 2)
    y_label = 'PC2(%s%%)' % round((pca.explained_variance_ratio_[1] * 100), 2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    file_name = 'DBSCAN' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    plt.close()

    file_path = '\\static\\PythonPlot\\' + file_name

    return file_path