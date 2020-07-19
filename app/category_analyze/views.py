# _*_ coding: UTF-8 _*_

from flask import render_template, request, jsonify
import json
import pandas as pd
import numpy as np
from app import mongo
from app.util.methods.category_analyze import def_GNB, def_KNN, def_hierarchy, def_kmeans, def_DBSCAN, def_fisher
from . import category_analyze

#显示页面
@category_analyze.route('/category_analyze/<method_index>/')
def return_category_analyze_html(method_index):
    return render_template('category_analyze/category_analyze.html', name=method_index)

#查看数据集
@category_analyze.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#选择数据集
@category_analyze.route('/category_analyze/data/selectdata/', methods=['POST'])
def select_data():
    data_file_name = request.values.get('file_name')
    data_file_features = mongo.db.base_features.find_one({'file_name': data_file_name}, {'_id': 0})['cols']
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0})))
    data = list(json.loads(data.head(10).T.to_json()).values())
    if len(data_file_features) > 0:
        res = {'status': 1, 'file_features': data_file_features, 'data': data}
    else:
        res = {'status': 0}
    return jsonify(res)

# 计算结果
@category_analyze.route('/category_analyze/data/compute/', methods=['POST'])
def compute_data():
    #取得文件名
    data_file_name = request.values.get('file_name')
    #取得方法名
    data_file_method = request.values.get('file_method')
    #取得变量X
    data_file_featureX = request.values.getlist('file_featureX[]')
    #取得变量Y
    data_file_featureY = request.values.getlist('file_featureY[]')
    #
    data_file_features = request.values.getlist('file_features[]')
    #不超过数据集的总样本数
    data_file_parameter_sum = request.values.get('file_parameter_sum')
    data_file_selectedSimilarOption = request.values.getlist('file_selectedSimilarOption[]')
    data_file_parameter_eps = request.values.get('file_parameter_eps')
    data_file_parameter_minSum = request.values.get('file_parameter_minSum')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))
    data_rows = data.shape[0]

    similarOption = {'类间最小距离': 'ward', '类间最大距离': 'complete', '类间平均距离': 'average', '最近邻点距离': 'single'}

    result = []
    result_labels_cols = []
    result_labels_list = []
    result_summary_cols = []
    result_summary = []
    result_centers_cols = []
    result_centers_list = []
    #报bug
    result_plot = []
    result_summary_plus_cols = []
    result_summary_plus = []

    #贝叶斯分类
    if data_file_method == '11':
        result = list(def_GNB(np.array(data[data_file_featureX]), np.array(data[data_file_featureY[0]])))
    # KNN分类
    if data_file_method == '12':
        result = list(def_KNN(np.array(data[data_file_featureX]), np.array(data[data_file_featureY[0]]),
                              eval(data_file_parameter_sum)))
    # 线性判别
    if data_file_method == '13':
        result = list(def_fisher(np.array(data[data_file_featureX]), np.array(data[data_file_featureY[0]])))

    if data_file_method in ['11', '12', '13']:
        [result_labels_cols, result_labels_list] = labels_to_dict(result[0], data_rows, data_file_method)
        result_1_summary = pd.DataFrame([result[1]])
        if not list(result_1_summary.columns)[0]:
            result_1_summary.columns = ['错误个数', '正确个数', '正确率']
            true_list = result_1_summary['正确个数']
            result_1_summary = result_1_summary.drop('正确个数', axis=1)
            result_1_summary.insert(0, '正确个数', true_list)
        else:
            result_1_summary.columns = ['正确个数', '错误个数',  '正确率']
        result_summary_cols = list(result_1_summary.columns)
        result_summary = result_1_summary.to_dict(orient='records')

        result_dict = result[2]
        dict_list = []
        for key, value in result_dict.items():
            dict_list.append((str(key), value))
        dict_list = sorted(dict_list, key=lambda d: int(d[0]))
        result_dict = {}
        for i in range(len(dict_list)):
            result_dict[dict_list[i][0]] = dict_list[i][1]
        result_summary_plus = pd.DataFrame([result_dict], columns=result_dict.keys(), dtype=float)
        result_summary_plus.insert(0, '分类标签 ', ['分类个数'])
        result_summary_plus_cols = list(result_summary_plus.columns)
        result_summary_plus = result_summary_plus.to_dict(orient='records')

    #系统聚类
    if data_file_method == '21':
        [result_labels, result_file_path1, result_file_path2, result_dict] = def_hierarchy(data[data_file_features],
                                                                                  eval(data_file_parameter_sum),
                                                                                  similarOption[data_file_selectedSimilarOption[0]])
        [result_labels_cols, result_labels_list] = labels_to_dict(result_labels, data_rows, data_file_method)
        result_plot.append(result_file_path1)
        result_plot.append(result_file_path2)
        [result_summary_cols, result_summary] = summary_to_dict(result_dict)

    #K平均值聚类
    if data_file_method == '22':
        [result_centers, result_labels, result_file_path1, result_dict] = def_kmeans(data[data_file_features],
                                                                                     eval(data_file_parameter_sum))
        result_centers = pd.DataFrame(result_centers, columns=data_file_features, index=['类' + str(x) for x in range(1, eval(data_file_parameter_sum)+1)])
        result_centers = result_centers.applymap("{0:.04f}".format)
        result_centers.insert(0, ' ', result_centers.index, allow_duplicates=True)
        result_centers_cols = list(result_centers.columns)
        result_centers_list = result_centers.to_dict(orient='records')
        [result_labels_cols, result_labels_list] = labels_to_dict(result_labels, data_rows, data_file_method)
        result_plot.append(result_file_path1)
        [result_summary_cols, result_summary] = summary_to_dict(result_dict)

    #DBSCAN聚类
    if data_file_method == '23':
        [result_labels, result_file_path1, result_dict] = def_DBSCAN(data[data_file_features], eval(data_file_parameter_eps),
                                                                     eval(data_file_parameter_minSum))
        [result_labels_cols, result_labels_list] = labels_to_dict(result_labels, data_rows, data_file_method)
        result_plot.append(result_file_path1)
        [result_summary_cols, result_summary] = summary_to_dict(result_dict)

    res = {'status': 1, 'labels_cols': result_labels_cols, 'result_labels': result_labels_list, 'centers_cols':
           result_centers_cols, 'result_centers': result_centers_list, 'plot_lists': result_plot, 'result_summary_cols':
           result_summary_cols, 'result_summary': result_summary, 'result_summary_plus_cols': result_summary_plus_cols,
           'result_summary_plus': result_summary_plus}

    return jsonify(res)


def labels_to_dict(result_labels, data_rows, method_name):
    if method_name in ['11', '12', '13']:
        result_labels = pd.DataFrame(result_labels, columns=['分类标签'], index=list(range(1, data_rows+1)),
                                     dtype=np.float)
    else:
        result_labels = pd.DataFrame(result_labels, columns=['聚类标签'], index=list(range(1, data_rows+1)),
                                     dtype=np.float)
    result_labels.insert(0, ' ', result_labels.index, allow_duplicates=True)
    result_labels_cols = list(result_labels.columns)
    result_labels_list = result_labels.to_dict(orient='records')

    return result_labels_cols, result_labels_list


def summary_to_dict(result_dict):
    dict_list = []
    for key, value in result_dict.items():
        dict_list.append((str(key), value))
    dict_list = sorted(dict_list, key=lambda d:int(d[0]))
    result_dict = {}
    for i in range(len(dict_list)):
        result_dict[dict_list[i][0]] = dict_list[i][1]
    result_summary = pd.DataFrame([result_dict], columns=result_dict.keys())
    result_summary.index = ['个数']
    result_summary.insert(0, '标签', list(result_summary.index))
    result_summary_cols = list(result_summary.columns)
    result_summary = result_summary.to_dict(orient='records')

    return result_summary_cols, result_summary

