# _*_ coding: UTF-8 _*_
from bson import ObjectId

from flask import render_template, redirect, url_for, request, session, jsonify, make_response
import json
import pandas as pd
import numpy as np


from app import mongo
from app.util import allowed_file
from app.util.methods.data_preprocessing import scaled, diff, log_data
from app.util.methods.import_description import def_mode, def_median, def_quantile, def_mean, def_ptp, def_var, def_varBias, \
     def_std, def_CV, def_skew, def_kurt,def_cov, def_covBias, def_corrcoef
from . import import_description


#显示数值分析页面
@import_description.route('/import_description/description_analyze/')
def return_description_analyze_html():
    return render_template('import_description/description_analyze.html', name='description_analyze_html')

#显示图分析页面
@import_description.route('/import_description/description_plot/<method_index>/')
def return_description_plot_html(method_index):
    return render_template('import_description/description_plot.html', name=method_index)

#######################################################################################################################
#选择数据集
@import_description.route('/import_description/data/selectdata/', methods=['POST'])
def select_data():

    #取得文件名
    data_file_name = request.values.get('file_name')
    #从数据库中查找对应的数据返回前十条
    data_file_features = mongo.db.base_features.find_one({'file_name': data_file_name}, {'_id': 0})['cols']
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0})))
    data = list(json.loads(data.head(10).T.to_json()).values())
    if len(data_file_features) > 0:
        res = {'status': 1, 'file_features': data_file_features, 'data': data}
    else:
        res = {'status': 0}
    return jsonify(res)

#查看数据
@import_description.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#计算数据
@import_description.route('/import_description/data/compute/', methods=['POST'])
def compute_data():
    #取得 文件名
    data_file_name = request.values.get('file_name')
    #取得 选择的序列
    data_file_featureList = request.values.getlist('file_feature[]')
    #取得 集中趋势
    data_file_trendList = request.values.getlist('file_trendList[]')
    #取得 分位点
    data_file_prameter_p = request.values.get('file_prameter_p')
    #取得 离散程度
    data_file_discreteList = request.values.getlist('file_discreteList[]')
    #取得 分布形状
    data_file_distributedList = request.values.getlist('file_distributedList[]')
    #取得 相关程度
    data_file_corList = request.values.getlist('file_corList[]')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))
    data_feature = data[data_file_featureList]

    trend_list = ['def_mean', 'def_median', 'def_mode', 'def_quantile']
    discrete_list = ['def_ptp', 'def_varBias', 'def_var', 'def_std', 'def_CV']
    distribute_list = ['def_skew', 'def_kurt']
    result_trend = pd.DataFrame()
    result_discrete = pd.DataFrame()
    result_distribute = pd.DataFrame()
    for column, feature in data_feature.iteritems():
        list1 = []
        if type(feature[0]) != str:
            for trend in trend_list:
                if trend in data_file_trendList:
                    if trend == 'def_quantile':
                        list1.append(def_quantile(list(feature), eval(data_file_prameter_p)))
                    else:
                        list1.append(float(eval(trend)(list(feature))))
            result_trend[column] = list1
        if type(feature[0]) == str and 'def_mode' in data_file_trendList:
            list1.append('NaN')
            list1.append('NaN')
            list1.append(def_mode(list(feature)))
            result_trend[column] = list1

        if type(feature[0]) != str:
            list2 = []
            for discrete in discrete_list:
                if discrete in data_file_discreteList:
                    list2.append(float(eval(discrete)(list(feature))))
            result_discrete[column] = list2

            list3 = []
            for distribute in distribute_list:
                if distribute in data_file_distributedList:
                    list3.append(eval(distribute)(list(feature)))
            result_distribute[column] = list3

    trend_dict = {'def_mean': '均值', 'def_median': '中位数', 'def_mode': '众数', 'def_quantile': '分位数'}
    discrete_dict = {'def_ptp': '极差', 'def_varBias': '方差(有偏估计)', 'def_var': '方差(无偏估计)', 'def_std': '标准差',
                     'def_CV': '变异系数'}
    distribute_dict = {'def_skew': '偏态系数', 'def_kurt': '峰态系数'}
    trend_index = []
    discrete_index = []
    distribute_index = []
    for key in trend_dict:
        for item in data_file_trendList:
            if key == item:
                trend_index.append(trend_dict[key])
    result_trend = result_trend.applymap("{0:.04f}".format)
    result_trend.insert(0, '集中趋势', trend_index, allow_duplicates=True)
    result_trend_features = list(result_trend.columns)
    result_trend = result_trend.to_dict(orient='records')

    for key in discrete_dict:
        for item in data_file_discreteList:
            if key == item:
                discrete_index.append(discrete_dict[key])
    result_discrete = result_discrete.applymap("{0:.04f}".format)
    result_discrete.insert(0, '离散程度', discrete_index, allow_duplicates=True)
    result_discrete_features = list(result_discrete.columns)
    result_discrete = result_discrete.to_dict(orient='records')

    for key in distribute_dict:
        for item in data_file_distributedList:
            if key == item:
                distribute_index.append(distribute_dict[key])
    result_distribute = result_distribute.applymap("{0:.04f}".format)
    result_distribute.insert(0, '分布形状', distribute_index, allow_duplicates=True)
    result_distribute_features = list(result_distribute.columns)
    result_distribute = result_distribute.to_dict(orient='records')

    drop_list = []
    for columns, feature in data_feature.iteritems():
        if type(feature[0]) == str:
            drop_list.append(columns)
            data_file_featureList.remove(columns)
    data_feature = data_feature.drop(drop_list, axis=1)

    data_featureList = []
    for column, feature in data_feature.iteritems():
        data_featureList.append(list(feature))

    result_covbias_features = []
    result_covbias = []
    result_cov_features = []
    result_cov = []
    result_cor_features = []
    result_cor = []

    if len(data_file_featureList) > 1:
        if 'def_covBias' in data_file_corList:
            result_covbias = pd.DataFrame(def_covBias(data_featureList), columns=data_file_featureList)
            result_covbias = result_covbias.applymap("{0:.04f}".format)
            result_covbias.insert(0, '协方差（有偏估计）', data_file_featureList, allow_duplicates=True)
            result_covbias_features = list(result_covbias.columns)
            result_covbias = result_covbias.to_dict(orient='records')
        if 'def_cov' in data_file_corList:
            result_cov = pd.DataFrame(def_cov(data_featureList), columns=data_file_featureList)
            result_cov = result_cov.applymap("{0:.04f}".format)
            result_cov.insert(0, '协方差（无偏估计）', data_file_featureList, allow_duplicates=True)
            result_cov_features = list(result_cov.columns)
            result_cov = result_cov.to_dict(orient='records')

        if 'def_corrcoef' in data_file_corList:
            cor_data = def_corrcoef(data_featureList)
            cor_data[0][0] = 1
            result_cor = pd.DataFrame(cor_data, columns=data_file_featureList)
            result_cor = result_cor.applymap("{0:.04f}".format)
            result_cor.insert(0, '相关系数', data_file_featureList, allow_duplicates=True)
            result_cor_features = list(result_cor.columns)
            result_cor = result_cor.to_dict(orient='records')

    res = {'status': 1, 'trendCols': result_trend_features, 'trend': result_trend, 'discreteCols':
           result_discrete_features, 'discrete': result_discrete, 'distributeCols': result_distribute_features,
           'distribute': result_distribute, 'covBiasCols': result_covbias_features, 'covBias': result_covbias,
           'covCols': result_cov_features, 'cov': result_cov, 'corCols': result_cor_features, 'cor': result_cor}

    return jsonify(res)

#利用数据绘图
@import_description.route('/import_description/data/compute/plot/', methods=['POST'])
def data_compute_plot():
    #取得文件名
    data_file_name = request.values.get('file_name')
    #取得方法名
    data_file_method = request.values.get('file_method')
    #取得参数
    data_file_feature1 = request.values.getlist('file_feature1[]')
    data_file_feature2 = request.values.getlist('file_feature2[]')
    data_file_features = request.values.getlist('file_features[]')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))

    result_data = []
    if data_file_method == '21' or data_file_method == '22' or data_file_method == '23':
        result_data = list(data[data_file_feature1[0]])
    if data_file_method == '24':
        result_data = np.array(data[data_file_feature2].values).tolist()
    if data_file_method == '25':
        result_data = np.array(data[data_file_features].T.values).tolist()

    res = {'status': 1, 'result_data': result_data}

    return jsonify(res)

#######################################################################################################################
#创建note
@import_description.route('/import_description/create_note/', methods=['POST'])
def create_note():
    name = request.values.get('name')
    note = {'name': name}
    data_note = mongo.db.note.find_one({'name': name})
    if(data_note):
        res = {'status': 0}
    else:
        mongo.db.note.insert(note)
        res = {'status': 1}
    return jsonify(res)

#保存note
@import_description.route('/import_description/save_note/', methods=['POST'])
def save_note():
    name = request.values.get('name')
    content = request.values.get('content')
    mongo.db.note.update({'name': name}, {'$set': {'content': content}})
    res = {'status': 1}
    return jsonify(res)

# #查找note
# @import_description.route('/import_description/search_note/', methods=['POST'])
# def search_note():
#     name = request.values.get('name')
#     data_note = mongo.db.note.find_one({'name': name},{'content':1,'_id':0})
#     note = data_note['content']
#     res = {'status': 1, 'result':note}
#     return jsonify(res)

#查找note
@import_description.route('/import_description/search_note/', methods=['POST'])
def search_note():
    name = request.values.get('name')
    data_note = mongo.db.note.find_one({'name': name})
    res = {'status': 1, 'result': data_note.get('content')}
    return jsonify(res)

#查看note
@import_description.route('/import_description/find_note/', methods=['POST'])
def find_note():
    name = request.values.get('name')
    data_note = mongo.db.note.find_one({'name': name})
    res = {'status': 1, 'result': data_note.get('content')}
    return jsonify(res)

#删除note
@import_description.route('/import_description/delete_note/', methods=['POST'])
def delete_note():
    del_note_name = request.values.get('del_note_name')
    mongo.db.note.delete_many({'name': del_note_name})

    res = {'status': 1}

    return jsonify(res)

#从数据库读取note展示列表
@import_description.route('/import_description/note/init/', methods=['POST'])
def notes_list():
    item = list(mongo.db.note.find({}, {'name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['name']))
        res = {'status': 1, 'notes': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#######################################################################################################################
#上传文件
@import_description.route('/import_description/data/upload/', methods=['POST'])
def upload_data():
    file_final_name = request.values.get('fileName')
    update_signal = request.values.getlist('updateSignal')
    file = request.files['file']
    if not file:
        res = {
            'status': 0,
            'msg': '请选择文件'
        }
        return jsonify(res)
    file_name = file.filename
    if not allowed_file(file_name):
        res = {
            'status': 0,
            'msg': '文件格式不正确'
        }
        return jsonify(res)
    else:
        file_extend = file_name.rsplit('.', 1)[1]
        if file_extend == 'xls' or file_extend == 'xlsx':
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        cols = df.columns.values.tolist()
        df['file_name'] = file_final_name
        records = json.loads(df.T.to_json()).values()
        if update_signal:
            mongo.db.base_datas.delete_many({'file_name': file_final_name})
            mongo.db.base_datas.insert(records)
            mongo.db.base_features.delete_many({'file_name': file_final_name})
            mongo.db.base_features.insert({'file_name': file_final_name, 'cols': cols})
        else:
            mongo.db.base_datas.insert(records)
            mongo.db.base_features.insert({'file_name': file_final_name, 'cols': cols})

        res = {
            'status': 1,
        }
        return jsonify(res)

#弹窗展示文件内的数据
@import_description.route('/import/data/basic_description/', methods=['POST'])
def import_basic_description():
    data_file_name = request.values.get('file_name')
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))
    (row_num, col_num) = data.shape
    cols = data.columns.values.tolist()
    head_datas = list(json.loads(data.head(10).T.to_json()).values())
    [basic_feature_description, fea_cols] = calculate_basic_features(data)

    res = {
        'status': 1,
        'row_num': row_num,
        'col_num': col_num,
        'cols': cols,
        'head_datas': head_datas,
        'basic_cols': fea_cols,
        'basic_description': basic_feature_description,
    }

    return jsonify(res)

#删除文件
@import_description.route('/import/data/deleteData/', methods=['POST'])
def delete_data():
    data_file_delDataName = request.values.get('file_delDataName')
    mongo.db.base_datas.delete_many({'file_name': data_file_delDataName})
    mongo.db.base_features.delete_many({'file_name': data_file_delDataName})

    res = {'status': 1}

    return jsonify(res)

#在弹窗运算数据时调用此方法
@import_description.route('/import/data/preprocess/', methods=['POST'])
def compute_preprocess():
    data_file_name = request.values.get('file_name')
    data_file_dataFields = request.values.getlist('file_dataFields[]')
    data_file_preProcessingList = request.values.getlist('file_preProcessingList[]')
    data_file_diffParameter = request.values.get('file_diffParameter')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))

    result = []
    if data_file_preProcessingList[0] == 'scaled':
        result = pd.DataFrame(scaled(np.array(data[data_file_dataFields])), columns=data_file_dataFields)
        for column in data_file_dataFields:
            data[column] = result[column].values

    if data_file_preProcessingList[0] == 'diff':
        result = diff(data[data_file_dataFields], eval(data_file_diffParameter))
        start = list(result.index)[0]
        end = list(result.index)[-1]
        data = data[start:end+1]
        for column in data_file_dataFields:
            data[column] = result[column].values

    if data_file_preProcessingList[0] == 'log_data':
        for field in data_file_dataFields:
            result.append(log_data(np.array(data[field])))
        result = pd.DataFrame(result, index=data_file_dataFields).T
        for column in data_file_dataFields:
            data[column] = result[column].values

    process_resultCols = list(data.columns)
    process_result = data.to_dict(orient='records')

    res = {'status': 1, 'process_resultCols': process_resultCols, 'process_result': process_result}

    return jsonify(res)

#将弹窗对数据集操作后的结果保存为新文件
@import_description.route('/import/data/saveNewData/', methods=['POST'])
def save_data():
    data_file_saveFileNameParameter = request.values.get('file_saveFileNameParameter')
    data_file_process_result = request.values.get('file_process_result')

    save_data = pd.DataFrame(json.loads(data_file_process_result))
    cols = list(save_data.columns)
    save_data['file_name'] = data_file_saveFileNameParameter
    records = json.loads(save_data.T.to_json()).values()

    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        if data_file_saveFileNameParameter in item:
            mongo.db.base_datas.delete_many({'file_name': data_file_saveFileNameParameter})
            mongo.db.base_datas.insert(records)

            mongo.db.base_features.delete_many({'file_name': data_file_saveFileNameParameter})
            mongo.db.base_features.insert({'file_name': data_file_saveFileNameParameter, 'cols': cols})
        else:
            mongo.db.base_datas.insert(records)
            mongo.db.base_features.insert({'file_name': data_file_saveFileNameParameter, 'cols': cols})

    res = {'status': 1}

    return jsonify(res)

#######################################################################################################################
#获取知识库的列表
@import_description.route('/import_description/get_knowledge_menu/', methods=['POST'])
def get_knowledge_menu():
    data = list(mongo.db.knowledge_base.find({}, {'_id': 1, 'name': 1, 'parent_id': 1, 'type': 1,'icon':1}))
    for menu in data:
        menu['_id'] = str(menu['_id'])
    data_tree = []
    data_linear = data

    for i in data_linear:
        if i['parent_id'][-1] == '0':
            dict_list = {'label': i['name'], 'value': i['_id'], 'type': i['type'], 'icon': i['icon']}
            data_tree.append(to_tree_children(dict_list, data_linear))

        res = {'status': 1,  'data_tree': data_tree}
        return jsonify(res)

#获取知识点
@import_description.route('/import_description/analyse_markdown/', methods=['POST'])
def analyse_markdown():

    id = request.values.get('id')
    knowledge_base = mongo.db.knowledge_base.find_one({'_id': ObjectId(id)})
    path = ['\\static\\PythonPlot\\' + knowledge_base.get('url')]

    try:
        f_name = open(path).read()
        res = {'status': 1, 'result': f_name}
        return jsonify(res)
    except OSError as reason:
        print('读取文件出错了T_T')
        print('出错原因是%s' % str(reason))

#######################################################################################################################
#
def to_tree_children(list, data_linear):
    for i in data_linear:
        if i['parent_id'][-1] == list['value']:
            dict_list = {'label': i['name'], 'value': i['_id'], 'type': i['type'], 'icon': i['icon']}
            if 'children' not in list:
                list['children'] = []
                list['children'].append(dict_list)
            else:
                list['children'].append(dict_list)

    if 'children' in list:
        for j in list['children']:
            to_tree_children(j, data_linear)

    return list

#######################################################################################################################
def calculate_basic_features(features):
    feature_data = []
    feature_columns = []
    for index, row in features.iteritems():
        # todo  判断是数字否
        feature = row.dropna()
        missing_number = len(row) - len(feature)
        max_value = max(feature)
        min_value = min(feature)
        if type(row[0]) != str:
            median_value = def_median(feature)
            avg_value = def_mean(feature)
            sd_value = def_std(feature)
            initial_number_feature = {'最大值': max_value, '最小值': min_value, '平均值': avg_value,
                                      '中位数': median_value, '标准差': sd_value, '缺失值数量': missing_number}
            feature_data.append(initial_number_feature)
            feature_columns.append(index)

    feature_data = pd.DataFrame(feature_data, dtype=float).T
    feature_data = feature_data.applymap("{0:.04f}".format)
    feature_data.columns = feature_columns
    feature_data.insert(0, '基本特征', list(feature_data.index), allow_duplicates=True)
    fea_cols = list(feature_data.columns)
    feature_data_list = feature_data.to_dict(orient='records')

    return feature_data_list, fea_cols
