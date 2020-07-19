# _*_ coding: UTF-8 _*_

import os
import time

from sklearn.decomposition import PCA
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from numpy import cumsum

#主成分分析
def def_pca(X, k):
    model = PCA(n_components=k)
    model.fit(X)

    explained_variance = model.explained_variance_
    explained_variance_ratio_ = model.explained_variance_ratio_
    cumsum_explained_variance_ratio_ = cumsum(explained_variance_ratio_)
    components = model.components_
    transform = model.fit_transform(X)
    score = model.score_samples(X)
    score_avg = model.score(X)

    plt.figure()
    plt.scatter(transform[:, 0], transform[:, 1])
    for i in range(transform[:0].size):
        plt.text(transform[i, 0], transform[i, 1], X.index[i])
    x_label = 'PC1(%s%%)' % round((model.explained_variance_ratio_[0] * 100), 2)
    y_label = 'PC2(%s%%)' % round((model.explained_variance_ratio_[1] * 100), 2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    file_name = 'plot_pca' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    result_PCA_path = '\\static\\PythonPlot\\' + file_name
    plt.close()

    return explained_variance, explained_variance_ratio_, cumsum_explained_variance_ratio_, components, transform, score, score_avg, result_PCA_path

#因子分析
def def_factor_analysis(X, k, rotation_=None):
    model = FactorAnalyzer(n_factors=k, rotation=rotation_).fit(X)

    eigen = model.get_eigenvalues()
    l = model.loadings_
    v = model.get_factor_variance()

    return eigen, l, v

