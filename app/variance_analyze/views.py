# _*_ coding: UTF-8 _*_

from flask import render_template, request, jsonify
import json
import pandas as pd
from app import mongo
from app.util.methods.variance_analyze import aov_oneway, aov_twoway_cross, aov_twoway, aov_multiway, aov_multiway_cross
from . import variance_analyze

#主页
@variance_analyze.route('/variance_analyze/<method_index>/')
def return_variance_analyze_html(method_index):
    return render_template('variance_analyze/variance_analyze.html', name=method_index)

#选择数据集
@variance_analyze.route('/variance_analyze/data/selectdata/', methods=['POST'])
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

#显示数据
@variance_analyze.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#计算数据
@variance_analyze.route('/variance_analyze/data/compute/', methods=['POST'])
def compute_data():
    data_file_name = request.values.get('file_name')
    data_file_method = request.values.get('file_method')
    data_file_featureX = request.values.getlist('file_featureX[]')
    data_file_featureY = request.values.getlist('file_featureY[]')
    data_file_boolOption = request.values.getlist('file_boolOption[]')
    data_file_interactionBoolOption = request.values.getlist('file_interactionBoolOption[]')
    data_file_interactionParameter = request.values.get('file_interactionParameter')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))

    cols = []
    result_variance = []
    if data_file_method == '1':
        data_featureX = data[[data_file_featureX[0]]]
        data_featureY = data[[data_file_featureY[0]]]
        result = aov_oneway(data_featureX, data_featureY)
        [cols, result_variance] = update_result(result)

    if data_file_method == '2':
        data_featureX12 = data[[data_file_featureX[0], data_file_featureX[1]]]
        data_featureY = data[[data_file_featureY[0]]]
        if data_file_boolOption[0] == '是':
            result = aov_twoway_cross(data_featureX12, data_featureY)
        else:
            result = aov_twoway(data_featureX12, data_featureY)
        [cols, result_variance] = update_result(result)

    if data_file_method == '3':
        data_featureXs = data[data_file_featureX]
        data_featureY = data[[data_file_featureY[0]]]
        result = []
        if data_file_boolOption[0] == '是':
            if data_file_interactionBoolOption[0] == 'all':
                interactionParameter = []
                for i in range(0, len(data_file_featureX)):
                    for j in range(i+1, len(data_file_featureX)):
                        interactionParameter.append(str(data_file_featureX[i] + ':' + data_file_featureX[j]))
                result = aov_multiway_cross(data_featureXs, data_featureY, *interactionParameter)
            if data_file_interactionBoolOption[0] == 'customize':
                interactionParameter = data_file_interactionParameter.split(',')
                result = aov_multiway_cross(data_featureXs, data_featureY, *interactionParameter)
        else:
            result = aov_multiway(data_featureXs, data_featureY)
        [cols, result_variance] = update_result(result)

    res = {'status': 1, 'col': cols, 'result': result_variance}

    return jsonify(res)

#返回结果
def update_result(result):
    result = result.applymap("{0:.04f}".format)
    result.insert(0, 'result', list(result.index), allow_duplicates=True)
    result_plus = result.fillna('NaN')
    cols = list(result_plus.columns)
    result_variance = result_plus.to_dict(orient='records')

    return cols, result_variance
