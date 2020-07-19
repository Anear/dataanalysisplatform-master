# _*_ coding: UTF-8 _*_

from flask import render_template, request, jsonify
import json
import pandas as pd
import numpy as np
from app import mongo
from app.util.methods.statistics_test import def_pearsonr, def_spearman, def_kendalltau, def_ttest_1samp, def_ttest_ind, \
    def_ttest_rel, def_chisquare, def_table, def_mannwhitneyu, def_wilcoxon, def_kruskal, def_friedmanchisquare, \
    def_shapiro, def_normaltest, def_anderson, def_kstest, def_bartlett, def_levene, def_fligner, def_runstest
from . import basic_test


#路由为/basic_test/参数传入method_index，可对参数做类型限定：<int：method_index>,只接受整形参数
@basic_test.route('/basic_test/<method_index>/')
def return_basic_test_html(method_index):
    return render_template('basic_test/basic_test.html', name=method_index)


@basic_test.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)


#选择数据集
@basic_test.route('/basic_test/data/selectdata/', methods=['POST'])
def select_data():
    #取得数据集名称
    data_file_name = request.values.get('file_name')
    #从数据库中取出用户选中的数据列,预览前十行返回
    data_file_features = mongo.db.base_features.find_one({'file_name': data_file_name}, {'_id': 0})['cols']
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0})))
    data = list(json.loads(data.head(10).T.to_json()).values())
    #判断是否取出数据
    if len(data_file_features) > 0:
        res = {'status': 1, 'file_features': data_file_features, 'data': data}
    else:
        res = {'status': 0}
    return jsonify(res)


#判断用户选择的计算方式，跳转相应方法返回计算结果
@basic_test.route('/basic_test/data/compute/', methods=['POST'])
def compute_data():
    #首先取得文件名
    data_file_name = request.values.get('file_name')
    #取得用户选择计算函数
    data_file_method = request.values.get('file_method')
    #取得用户操作的数据
    data_file_feature1 = request.values.getlist('file_feature1[]')
    data_file_feature2 = request.values.getlist('file_feature2[]')
    data_file_features = request.values.getlist('file_features[]')

    data_file_popMeanParameter = request.values.get('file_popMeanParameter')

    data_file_selectedBoolOption = request.values.getlist('file_selectedBoolOption[]')
    data_file_selectedFunctionOption_53 = request.values.getlist('file_selectedFunctionOption_53[]')
    data_file_selectedFunctionOption = request.values.getlist('file_selectedFunctionOption[]')

    data_file_parameter_a = request.values.get('file_parameter_a')
    data_file_parameter_b = request.values.get('file_parameter_b')
    data_file_parameter_u = request.values.get('file_parameter_u')
    data_file_parameter_sigma = request.values.get('file_parameter_sigma')
    data_file_parameter_t = request.values.get('file_parameter_t')
    data_file_selectedTestOption = request.values.getlist('file_selectedTestOption[]')
    data_file_selectedDivisionOption = request.values.getlist('file_selectedDivisionOption[]')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))

    boolOptions = {'是': True, '否': False}
    divisionOptions = {'均值': 'mean', '中位数': 'median', '自定义': 'customize'}
    testOptions = {'双尾检验': 'two-sided', '左尾检验': 'less', '右尾检验': 'greater'}
    functionOptions_53 = {'正态分布': 'norm', '指数分布': 'expon'}
    functionOptions = {'均匀分布': 'uniform', '正态分布': 'norm', '指数分布': 'expon'}

    results_2 = ['11', '12', '13', '31', '41', '42', '43', '44', '51', '52', '53', '54', '61', '62', '63', '71']
    results_6 = ['21', '22', '23']

    result = []
    cols = []
    result_statistic_test = []

    #皮尔森相关性系数
    if data_file_method == '13':
        result = list(def_pearsonr(np.array(data[data_file_feature2[0]]), np.array(data[data_file_feature2[1]])))

    # 斯皮尔曼相关性系数
    if data_file_method == '11':
        result = list(def_spearman(np.array(data[data_file_feature2])))

    # 肯德尔相关性系数
    if data_file_method == '12':
        result = list(def_kendalltau(np.array(data[data_file_feature2[0]]), np.array(data[data_file_feature2[1]])))

    # 单样本T检验
    if data_file_method == '21':
        result = list(def_ttest_1samp(data[data_file_feature1], float(eval(data_file_popMeanParameter))))

    # 两独立样本T检验
    if data_file_method == '22':
        result = list(def_ttest_ind(np.array(data[[data_file_feature2[0]]]), np.array(data[[data_file_feature2[1]]]),
                                    boolOptions[data_file_selectedBoolOption[0]]))

    # 两配对样本T检验
    if data_file_method == '23':
        result = list(def_ttest_rel(data[[data_file_feature2[0]]], data[[data_file_feature2[1]]]))

    # 曼—惠特尼U检验
    if data_file_method == '41':
        result = list(def_mannwhitneyu(np.array(data[data_file_feature2[0]]), np.array(data[data_file_feature2[1]]),
                      boolOptions[data_file_selectedBoolOption[0]], testOptions[data_file_selectedTestOption[0]]))

    # wilcoxon符号秩检验
    if data_file_method == '42':
        result = list(def_wilcoxon(np.array(data[data_file_feature2[0]]), np.array(data[data_file_feature2[1]]),
                      boolOptions[data_file_selectedBoolOption[0]]))

    # 克鲁什卡尔检验
    # 弗里德曼检验
    if data_file_method == '43' or data_file_method == '44':
        data_featureList = []
        data_feature = data[data_file_features]
        for column, feature in data_feature.iteritems():
            data_featureList.append(list(feature))
        if data_file_method == '43':
            result = list(def_friedmanchisquare(*data_featureList))
        if data_file_method == '44':
            result = list(def_kruskal(*data_featureList))

    # 正态分布检验
    if data_file_method == '51':
        result = list(def_normaltest(np.array(data[data_file_feature1[0]])))

    # 夏皮罗—威尔克检验
    if data_file_method == '52':
        result = list(def_shapiro(np.array(data[data_file_feature1[0]])))

    # 安德森检验
    if data_file_method == '53':
        result = list(def_anderson(np.array(data[data_file_feature1[0]]), functionOptions_53[data_file_selectedFunctionOption_53[0]]))

    # KS检验
    if data_file_method == '54':
        if functionOptions[data_file_selectedFunctionOption[0]] == 'uniform':
            result = list(def_kstest(np.array(data[data_file_feature1[0]]), functionOptions[data_file_selectedFunctionOption[0]],
                          (eval(data_file_parameter_a), eval(data_file_parameter_b)), testOptions[data_file_selectedTestOption[0]]))
        if functionOptions[data_file_selectedFunctionOption[0]] == 'norm':
            result = list(def_kstest(np.array(data[data_file_feature1[0]]), functionOptions[data_file_selectedFunctionOption[0]],
                          (eval(data_file_parameter_u), eval(data_file_parameter_sigma)), testOptions[data_file_selectedTestOption[0]]))
        if functionOptions[data_file_selectedFunctionOption[0]] == 'expon':
            result = list(def_kstest(np.array(data[data_file_feature1[0]]), functionOptions[data_file_selectedFunctionOption[0]],
                          (eval(data_file_parameter_t),), testOptions[data_file_selectedTestOption[0]]))

    # fligner—Killen检验
    # 巴特利检验
    # levene检验
    if data_file_method == '61' or data_file_method == '62' or data_file_method == '63':
        data_featureList = []
        data_feature = data[data_file_features]
        for column, feature in data_feature.iteritems():
            data_featureList.append(list(feature))
        if data_file_method == '61':
            result = list(def_fligner(*data_featureList))
        if data_file_method == '62':
            result = list(def_bartlett(*data_featureList))
        if data_file_method == '63':
            result = list(def_levene(*data_featureList))

    # 游程检验
    if data_file_method == '71':
        if divisionOptions[data_file_selectedDivisionOption[0]]:
            result = list(def_runstest(np.array(data[data_file_feature1[0]]), divisionOptions[data_file_selectedDivisionOption[0]],
                          boolOptions[data_file_selectedBoolOption[0]]))

    #判断方法，返回结果
    if data_file_method in results_2:
        #为数据加上字段
        result_statistic_test = pd.DataFrame(result, index=['统计量', 'P值']).T
        #结果保留四位小数
        result_statistic_test = result_statistic_test.applymap("{0:.04f}".format)
        #取得行数据
        cols = list(result_statistic_test.columns)
        #将结果存入列表类型的字典
        result_statistic_test = result_statistic_test.to_dict(orient='records')


    if data_file_method in results_6:
        result_plus = pd.DataFrame(result, index=['T统计量', '自由度', 'P值', '均值差值', '置信区间下限', '置信区间上限']).T
        result_plus = result_plus.applymap("{0:.04f}".format)
        result_statistic_test = result_plus.fillna('NaN')
        cols = list(result_statistic_test.columns)
        result_statistic_test = result_statistic_test.to_dict(orient='records')

    res = {'status': 1, 'col': cols, 'result': result_statistic_test}

    return jsonify(res)
