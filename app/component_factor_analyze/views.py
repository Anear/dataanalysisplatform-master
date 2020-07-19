# _*_ coding: UTF-8 _*_

from flask import render_template, request, jsonify
import json
import pandas as pd
import numpy as np
from app import mongo

from app.util.methods.component_factor_analyze import def_pca, def_factor_analysis
from . import component_factor_analyze

#显示页面
@component_factor_analyze.route('/component_factor_analyze/<method_index>/')
def return_component_factor_analyze_html(method_index):
    return render_template('component_factor_analyze/component_factor_analyze.html', name=method_index)

#查看数据
@component_factor_analyze.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#选择数据集
@component_factor_analyze.route('/component_factor_analyze/data/selectdata/', methods=['POST'])
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

#计算数据
@component_factor_analyze.route('/component_factor_analyze/data/compute/', methods=['POST'])
def compute_data():
    data_file_name = request.values.get('file_name')
    data_file_method = request.values.get('file_method')
    data_file_features = request.values.getlist('file_features[]')
    data_file_parameter = request.values.get('file_parameter')

    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))

    result_PCA_1_cols = []
    result_PCA_1 = []
    result_PCA_2_cols = []
    result_PCA_2 = []
    result_PCA_3_cols = []
    result_PCA_3 = []
    result_PCA_4_cols = []
    result_PCA_4 = []
    result_PCA_path = []
    result_factor_1_cols = []
    result_factor_1 = []
    result_factor_2_cols = []
    result_factor_2 = []
    result_factor_3_cols = []
    result_factor_3 = []
    if data_file_method == '1':
        result = def_pca(np.array(data[data_file_features]), eval(data_file_parameter))
        result_PCA_1 = pd.DataFrame([result[0], result[1], result[2]], columns=['主成分' + str(x) for x in range(1, eval(data_file_parameter) + 1)], index=['特征值', '贡献率', '累积贡献率']).T
        result_PCA_1 = result_PCA_1.applymap("{0:.04f}".format)
        result_PCA_1.insert(0, ' ', list(result_PCA_1.index))
        result_PCA_1_cols = list(result_PCA_1.columns)
        result_PCA_1 = result_PCA_1.to_dict(orient='records')

        result_PCA_2 = pd.DataFrame(result[3], columns=data_file_features, index=['主成分' + str(x) for x in range(1, eval(data_file_parameter) + 1)])
        result_PCA_2 = result_PCA_2.applymap("{0:.04f}".format)
        result_PCA_2.insert(0, ' ', list(result_PCA_2.index))
        result_PCA_2_cols = list(result_PCA_2.columns)
        result_PCA_2 = result_PCA_2.to_dict(orient='records')

        len_row = data.shape[0]

        index_rows = list(range(1, len_row + 1))
        result_PCA_3 = pd.DataFrame(result[4], columns=['主成分' + str(x) for x in range(1, eval(data_file_parameter) + 1)], index=index_rows)
        result_PCA_3 = result_PCA_3.applymap("{0:.04f}".format)
        result_PCA_3.insert(0, ' ', list(result_PCA_3.index))
        result_PCA_3_cols = list(result_PCA_3.columns)
        result_PCA_3 = result_PCA_3.to_dict(orient='records')

        result_5 = list(result[5])
        result_5.append(result[6])
        index_rows.append('mean')
        result_PCA_4 = pd.DataFrame(result_5, columns=['样本得分'], index=index_rows)
        result_PCA_4 = result_PCA_4.applymap("{0:.04f}".format)
        result_PCA_4.insert(0, ' ', list(result_PCA_4.index))
        result_PCA_4_cols = list(result_PCA_4.columns)
        result_PCA_4 = result_PCA_4.to_dict(orient='records')
        result_PCA_path.append(result[7])

    if data_file_method == '2':
        result = def_factor_analysis(np.array(data[data_file_features]), eval(data_file_parameter))
        result_factor_1 = pd.DataFrame(np.array(result[0]), index=['原始矩阵特征值', '公因子特征值'],
                                       columns=['特征' + str(x) for x in range(1, len(data_file_features) + 1)]).T
        result_factor_1 = result_factor_1.applymap("{0:.04f}".format)
        result_factor_1.insert(0, ' ', list(result_factor_1.index))
        result_factor_1_cols = list(result_factor_1.columns)
        result_factor_1 = result_factor_1.to_dict(orient='records')

        result_factor_2 = pd.DataFrame(np.array(result[1]),
                                       columns=['因子' + str(x) for x in range(1, eval(data_file_parameter) + 1)],
                                       index=data_file_features)
        result_factor_2 = result_factor_2.applymap("{0:.04f}".format)
        result_factor_2.insert(0, ' ', list(result_factor_2.index))
        result_factor_2_cols = list(result_factor_2.columns)
        result_factor_2 = result_factor_2.to_dict(orient='records')

        result_factor_3 = pd.DataFrame(np.array(result[2]), columns=['因子' + str(x) for x in range(1, eval(data_file_parameter) + 1)], index=['贡献率', '贡献率比例', '累积比例']).T
        result_factor_3 = result_factor_3.applymap("{0:.04f}".format)
        result_factor_3.insert(0, ' ', list(result_factor_3.index))
        result_factor_3_cols = list(result_factor_3.columns)
        result_factor_3 = result_factor_3.to_dict(orient='records')

    res = {'status': 1, 'result_PCA_1_cols': result_PCA_1_cols, 'result_PCA_1': result_PCA_1, 'result_PCA_2_cols':
           result_PCA_2_cols, 'result_PCA_2': result_PCA_2, 'result_PCA_3_cols': result_PCA_3_cols, 'result_PCA_3':
           result_PCA_3, 'result_PCA_4_cols': result_PCA_4_cols, 'result_PCA_4': result_PCA_4,
           'result_PCA_path': result_PCA_path, 'result_factor_1_cols': result_factor_1_cols, 'result_factor_1':
           result_factor_1, 'result_factor_2_cols': result_factor_2_cols, 'result_factor_2': result_factor_2,
           'result_factor_3_cols': result_factor_3_cols, 'result_factor_3': result_factor_3}

    return jsonify(res)
