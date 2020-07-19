# _*_ coding: UTF-8 _*_
from flask import render_template, request, jsonify
import json
import pandas as pd
import numpy as np
from app import mongo

from app.util.methods.time_series import def_adfuller, def_acorr_ljungbox, def_AR, def_MA, def_ARMA, def_ARIMA, \
    def_ARCH, def_decompose, def_plot, def_acfplot, def_pacfplot
from . import time_series

#显示页面
@time_series.route('/time_series/<method_index>/')
def return_time_series_html(method_index):
    return render_template('time_series/time_series.html', name=method_index)

#显示数据
@time_series.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#选择数据集
@time_series.route('/time_series/data/selectdata/', methods=['POST'])
def select_data():
    #取得传入的文件名存入data_file_name
    data_file_name = request.values.get('file_name')
    #从base_features表查file_name为data_file_name的cols的值，忽略id：
    # ['a','b','c','d','f','e']
    data_file_features = mongo.db.base_features.find_one({'file_name': data_file_name}, {'_id': 0})['cols']
    #从base_datas表查找file_name为data_file_name的值，忽略id
    # [{'a': 0.99999, 'b': 0.0109120232, 'c': 0.1587503038, 'd': 0.0144795471, 'e': 0.3984348176, 'f': 0.1587503038, 'file_name': 'data'},
    # {'a': 0.9863753028, 'b': 0.0150962024, 'c': 0.9527675892, 'd': 0.7418406001, 'e': 0.9760981453, 'f': 0.9527675892, 'file_name': 'data'},
    # {'a': 0.9458156724, 'b': 0.0150962024, 'c': 1.1238357159, 'd': 4.3943648452, 'e': 1.0601111809, 'f': 1.1238357159, 'file_name': 'data'},
    # {'a': 0.7791125862, 'b': 0.0170797664, 'c': 30.8887946795, 'd': 8.6350874773, 'e': 5.5577688581, 'f': 30.8887946795, 'file_name': 'data'},
    # {'a': 1.0327592648, 'b': 0.013139489, 'c': 5.5955425244, 'd': 6.6118583028, 'e': 2.3654899121, 'f': 5.5955425244, 'file_name': 'data'},
    # {'a': 1.1294267197, 'b': 0.0132390577, 'c': 7.5993325245, 'd': 8.2521091174, 'e': 2.7566886883, 'f': 7.5993325245, 'file_name': 'data'},
    # {'a': 0.9279602228, 'b': 0.0142711358, 'c': 8.8303592807, 'd': 10.0845951935, 'e': 2.9715920448, 'f': 8.8303592807, 'file_name': 'data'},
    # {'a': 0.9214689626, 'b': 0.0144865383, 'c': 9.8019143122, 'd': 5.0566104454, 'e': 3.1308009059, 'f': 9.8019143122, 'file_name': 'data'},
    # {'a': 0.9045593568, 'b': 0.0120845644, 'c': 4.9157505601, 'd': 6.8135768806, 'e': 2.2171491966, 'f': 4.9157505601, 'file_name': 'data'},
    # {'a': 0.8142516199, 'b': 0.0121559241, 'c': 4.2199339943, 'd': 15.2553800702, 'e': 4.2199339943, 'f': 17.8078429162, 'file_name': 'data'}]
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0})))
    #
    data = list(json.loads(data.head(10).T.to_json()).values())
    if len(data_file_features) > 0:
        res = {'status': 1, 'file_features': data_file_features, 'data': data}
    else:
        res = {'status': 0}
    return jsonify(res)

#计算数据
@time_series.route('/time_series/data/compute/', methods=['POST'])
def compute_data():
    #取得 文件名
    data_file_name = request.values.get('file_name')
    #取得 计算方法
    data_file_method = request.values.get('file_method')
    #取得 选择的序列
    data_file_feature = request.values.getlist('file_feature[]')


    #取得参数 maxlag
    data_file_parameter_maxlag = request.values.get('file_parameter_maxlag')
    #取得参数 alternative
    data_file_selectedAutoLag = request.values.getlist('file_selectedAutoLag[]')
    #取得参数 平均值
    data_file_selectedMean = request.values.getlist('file_selectedMean[]')
    #取得参数 lags
    data_file_parameter_lags = request.values.get('file_parameter_lags')
    #取得参数 vol
    data_file_selectedVol = request.values.getlist('file_selectedVol[]')
    #取得参数 p
    data_file_parameter_p = request.values.get('file_parameter_p')
    #取得参数 d
    data_file_parameter_d = request.values.get('file_parameter_d')
    #取得参数 o
    data_file_parameter_o = request.values.get('file_parameter_o')
    #取得参数 q
    data_file_parameter_q = request.values.get('file_parameter_q')
    #取得参数 预测步长
    data_file_parameter_step = request.values.get('file_parameter_step')
    #取得参数 dist
    data_file_selectedDist = request.values.getlist('file_selectedDist[]')
    #取得参数 model
    data_file_selectedModel = request.values.getlist('file_selectedModel[]')

    #从表base_datas中取出file_name为data_file_name的数据，忽略id和file_name
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0, 'file_name': 0})))
    #取出数据的列名
    data_feature = data[data_file_feature[0]]

    autoLagOptions = {'无': '', 'AIC': 'AIC', 'BIC': 'BIC', 't-stat': 't-stat'}
    meanOptions = {'常数': 'Constant', '零': 'Zero', 'ARX': 'ARX', 'HARX': 'HARX'}
    distOptions = {'正态分布': 'normal', '高斯分布': 'gaussian', 't分布': 't', 'skewt分布': 'skewt'}

    if data_file_selectedAutoLag:
        data_file_selectedAutoLag = autoLagOptions[data_file_selectedAutoLag[0]]
    if data_file_selectedMean:
        data_file_selectedMean = meanOptions[data_file_selectedMean[0]]
    if data_file_selectedDist:
        data_file_selectedDist = distOptions[data_file_selectedDist[0]]

    result_plot = []
    result_adfuller_1cols = []
    result_adfuller_1 = []
    result_adfuller_2cols = []
    result_adfuller_2 = []
    result_acorr_ljungboxcols = []
    result_acorr_ljungbox = []
    summary1cols = []
    summary1 = []
    summary2cols = []
    summary2 = []
    forecastcols = []
    forecast = []
    result_decomposecols = []
    result_decompose = []
    result_decompose_path = []

#######################################################################################################################
    #时序图
    if data_file_method == '11':
        result_plot = def_plot(data_feature)
    #ACF图
    if data_file_method == '12':
        result_plot = def_acfplot(data_feature)
    #PACF图
    if data_file_method == '13':
        result_plot = def_pacfplot(data_feature)
    #平稳性检验
    if data_file_method == '21':
        result = def_adfuller(data_feature, eval(data_file_parameter_maxlag), data_file_selectedAutoLag)
        if data_file_selectedAutoLag == '':
            result_adfuller_1 = pd.DataFrame([result[0], result[1], result[2], result[3]],
                                             index=['df', 'pvalue', 'usedlag', 'nobs']).T
            result_adfuller_1 = result_adfuller_1.applymap("{0:.04f}".format)
            result_adfuller_1cols = list(result_adfuller_1.columns)
            result_adfuller_1 = result_adfuller_1.to_dict(orient='records')
        else:
            result_adfuller_1 = pd.DataFrame([result[0], result[1], result[2], result[3], result[5]],
                                             index=['df', 'pvalue', 'usedlag', 'nobs', 'icbest']).T
            result_adfuller_1 = result_adfuller_1.applymap("{0:.04f}".format)
            result_adfuller_1cols = list(result_adfuller_1.columns)
            result_adfuller_1 = result_adfuller_1.to_dict(orient='records')
        result_adfuller_2 = pd.DataFrame([result[4]], columns=['1%', '5%', '10%'])
        result_adfuller_2 = result_adfuller_2.applymap("{0:.04f}".format)
        result_adfuller_2cols = list(result_adfuller_2.columns)
        result_adfuller_2 = result_adfuller_2.to_dict(orient='records')

    #白噪声检验
    if data_file_method == '22':
        result = def_acorr_ljungbox(data_feature, eval(data_file_parameter_lags))
        result_acorr_ljungbox = pd.DataFrame([result[0], result[1]], index=['qljungbox', 'pval']).T
        result_acorr_ljungbox = result_acorr_ljungbox.applymap("{0:.04f}".format)
        result_acorr_ljungboxcols = list(result_acorr_ljungbox.columns)
        result_acorr_ljungbox = result_acorr_ljungbox.to_dict(orient='records')

    #AR模型
    if data_file_method == '31':
        if data_file_parameter_step != '':
            result = def_AR(data_feature, eval(data_file_parameter_p), eval(data_file_parameter_step))
        else:
            result = def_AR(data_feature, eval(data_file_parameter_p))
        result_parse = parse_summary(result)
        summary1cols = result_parse[0]
        summary1 = result_parse[1]

        [summary2cols, summary2] = cols_final(result_parse[2], result_parse[3])

        forecast = pd.DataFrame([list(result[1][0]), list(result[1][1])], index=['预测值', '标准误差']).T
        confidence_interval = np.array(result[1][2])
        forecast['置信下区间'] = confidence_interval[:, 0]
        forecast['置信上区间'] = confidence_interval[:, 1]
        forecast = forecast.applymap("{0:.04f}".format)
        forecastcols = list(forecast.columns)
        forecast = forecast.to_dict(orient='records')

    #MA模型
    if data_file_method == '32':
        if data_file_parameter_step != '':
            result = def_MA(data_feature, eval(data_file_parameter_q), eval(data_file_parameter_step))
        else:
            result = def_MA(data_feature, eval(data_file_parameter_q))
        result_parse = parse_summary(result)
        summary1cols = result_parse[0]
        summary1 = result_parse[1]

        [summary2cols, summary2] = cols_final(result_parse[2], result_parse[3])

        forecast = pd.DataFrame([list(result[1][0]), list(result[1][1])], index=['预测值', '标准误差']).T
        confidence_interval = np.array(result[1][2])
        forecast['置信下区间'] = confidence_interval[:, 0]
        forecast['置信上区间'] = confidence_interval[:, 1]
        forecast = forecast.applymap("{0:.04f}".format)
        forecastcols = list(forecast.columns)
        forecast = forecast.to_dict(orient='records')

    #ARMA模型
    if data_file_method == '33':
        if data_file_parameter_step != '':
            result = def_ARMA(data_feature, eval(data_file_parameter_p), eval(data_file_parameter_q), eval(data_file_parameter_step))
        else:
            result = def_ARMA(data_feature, eval(data_file_parameter_p), eval(data_file_parameter_q))

        result_parse = parse_summary(result)
        summary1cols = result_parse[0]
        summary1 = result_parse[1]

        [summary2cols, summary2] = cols_final(result_parse[2], result_parse[3])

        forecast = pd.DataFrame([list(result[1][0]), list(result[1][1])], index=['预测值', '标准误差']).T
        confidence_interval = np.array(result[1][2])
        forecast['置信下区间'] = confidence_interval[:, 0]
        forecast['置信上区间'] = confidence_interval[:, 1]
        forecast = forecast.applymap("{0:.04f}".format)
        forecastcols = list(forecast.columns)
        forecast = forecast.to_dict(orient='records')

    #ARIMA模型
    if data_file_method == '34':
        result = def_ARIMA(data_feature, eval(data_file_parameter_p), eval(data_file_parameter_d), eval(data_file_parameter_q), eval(data_file_parameter_step))
        result_parse = parse_summary(result)
        summary1cols = result_parse[0]
        summary1 = result_parse[1]

        [summary2cols, summary2] = cols_final(result_parse[2], result_parse[3])

        forecast = pd.DataFrame([list(result[1][0]), list(result[1][1])], index=['预测值', '标准误差']).T
        confidence_interval = np.array(result[1][2])
        forecast['置信下区间'] = confidence_interval[:, 0]
        forecast['置信上区间'] = confidence_interval[:, 1]
        forecast = forecast.applymap("{0:.04f}".format)
        forecastcols = list(forecast.columns)
        forecast = forecast.to_dict(orient='records')

    # ARCH模型
    if data_file_method == '35':
        result = def_ARCH(data_feature, data_file_selectedMean, eval(data_file_parameter_lags), data_file_selectedVol[0],
                          eval(data_file_parameter_p), eval(data_file_parameter_o), eval(data_file_parameter_q),
                          data_file_selectedDist)
        summary1 = pd.DataFrame(result.tables[0].data[0:-1], columns=['1', '2', '3', '4'])
        summary1cols = list(summary1.columns)
        summary1 = summary1.to_dict(orient='records')

        summary2_data = result.tables[1].data[1:]
        for i in range(0, len(summary2_data)):
            summary2_data[i] = [x.replace(' ', '') for x in summary2_data[i]]
        summary2_columns = result.tables[1].data[0]
        summary2_columns[-1] = '95%置信区间'
        summary2_columns[0] = 'result'
        summary2 = pd.DataFrame(summary2_data, columns=summary2_columns)
        summary2cols = list(summary2.columns)
        summary2 = summary2.to_dict(orient='records')
        [summary2cols, summary2] = cols_final(summary2cols, summary2)

    #季节分解模型
    if data_file_method == '36':
        result = def_decompose(data_feature, data_file_selectedModel[0])
        result_decompose_init = pd.DataFrame(list(result[0:-1]), index=['trend', 'seasonal', 'resid', 'observed']).T
        result_decompose = result_decompose_init.fillna('NaN')
        result_decomposecols = list(result_decompose.columns)
        result_decompose = result_decompose.to_dict(orient='records')
        result_decompose_path = result[4]

    #将结果返回
    res = {'status': 1, 'result_plot': result_plot, 'result_adfuller_1cols': result_adfuller_1cols, 'result_adfuller_1':
           result_adfuller_1, 'result_adfuller_2cols': result_adfuller_2cols, 'result_adfuller_2': result_adfuller_2,
           'result_acorr_ljungboxcols': result_acorr_ljungboxcols, 'result_acorr_ljungbox': result_acorr_ljungbox,
           'summary1cols': summary1cols, 'summary1': summary1, 'summary2cols': summary2cols, 'summary2': summary2,
           'forecastcols': forecastcols, 'forecast': forecast, 'result_decomposecols': result_decomposecols,
           'result_decompose': result_decompose, 'result_decompose_path': result_decompose_path}

    return jsonify(res)

#######################################################################################################################
#ARIMA模型运算
def parse_summary(result):
    summary1 = pd.DataFrame(result[0].tables[0].data[0:-1], columns=['1', '2', '3', '4'])
    summary1cols = list(summary1.columns)
    summary1 = summary1.to_dict(orient='records')

    [summary2cols, summary2] = summary23_to_dict(result[0].tables[1].data[1:], result[0].tables[1].data[0])
    [summary3cols, summary3] = summary23_to_dict(result[0].tables[2].data[1:], result[0].tables[2].data[0])

    return summary1cols, summary1, summary2cols, summary2, summary3cols, summary3

#ARIMA模型运算函数
def summary23_to_dict(summary_data, summary_columns):
    for i in range(0, len(summary_data)):
        summary_data[i] = [x.replace(' ', '') for x in summary_data[i]]
    summary_columns[0] = 'result'
    summary = pd.DataFrame(summary_data, columns=summary_columns, dtype=float)
    index_list = list(summary['result'])
    summary = summary.drop(['result'], axis=1)
    summary.insert(0, 'result', index_list, allow_duplicates=True)
    summarycols = list(summary.columns)
    summary = summary.to_dict(orient='records')

    return summarycols, summary

#运算函数
def cols_final(cols, data):
    cols_final = []
    for col in cols:
        col_final = {"prop": col.replace('.', ''), 'label': col}
        cols_final.append(col_final)
    for row in data:
        for col in cols:
            row[col.replace('.', '')] = row[col]

    return cols_final, data


