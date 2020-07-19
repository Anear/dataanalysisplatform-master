# _*_ coding: UTF-8 _*_
import os

from flask import render_template, redirect, url_for, request, session, jsonify, make_response
import json
import pandas as pd
import time

from app import mongo
import matplotlib.pyplot as plt

from rpy2 import robjects

from app.util.methods.regression_analyze import def_lm, def_logit, def_PolReg, def_nonlinear
from . import regression_analyze

#显示页面
@regression_analyze.route('/regression_analyze/<method_index>/')
def return_regression_analyze_html(method_index):
    return render_template('regression_analyze/regression_analyze.html', name=method_index)

#查看数据
@regression_analyze.route('/import/data/init/', methods=['POST'])
def file_name_list():
    item = list(mongo.db.base_datas.find({}, {'file_name': 1, '_id': 0}))
    if len(item) > 0:
        item = list(set(pd.DataFrame(item)['file_name']))
        res = {'status': 1, 'file_names': item}
    else:
        res = {'status': 0}
    return jsonify(res)

#选择数据集
@regression_analyze.route('/regression_analyze/data/selectdata/', methods=['POST'])
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

#通过用户选择的方法计算数据
@regression_analyze.route('/regression_analyze/data/compute/', methods=['POST'])
def compute_data():
    #取得 文件名
    data_file_name = request.values.get('file_name')
    #取得 计算方法
    data_file_method = request.values.get('file_method')
    #取得 自变量X
    data_file_featureX = request.values.getlist('file_featureX[]')
    #取得 自变量Y
    data_file_featureY = request.values.getlist('file_featureY[]')[0]
    #取得 最高次幂
    data_file_parameterMax = request.values.get('file_parameterMax')
    #取得 回归方法
    data_file_alternative = request.values.getlist('file_alternative[]')
    #取得 参数名
    data_file_numberFormName = request.values.getlist('file_numberFormName[]')
    #取得 初始值
    data_file_numberFormValue = request.values.getlist('file_numberFormValue[]')
    #取得 非线性函数
    data_file_nonLinearFunction = request.values.get('file_nonLinearFunction')
    #从数据库中取得数据（表头+数据）
    data = pd.DataFrame(list(mongo.db.base_datas.find({'file_name': data_file_name}, {'_id': 0})))

    methodOptions = {'无': '无', '逐步法': 'both', '向前法': 'forward', '向后法': 'backward'}
    result_1residual_cols = []
    result_1residuals = []
    result_1Coefficients_cols_final = []
    result_1Coefficients = []
    result_1_summary_cols = []
    result_1_summary = []
    result_2cols_final = []
    result_2 = []
    result_34cols = []
    result_34 = []
    result_34_plot = []
    result_5cols = []
    result_5 = []
    result_6cols = []
    result_6 = []
    result_7cols = []
    result_7 = []
    result_8cols = []
    result_8 = []
    result_nonLinear_cols = []
    result_nonLinear = []

    # 取得回归方法
    if data_file_alternative:
        data_file_alternative = methodOptions[data_file_alternative[0]]

    #取得 自变量X，Y
    if data_file_featureX and data_file_featureY:
        X = {}
        for i in range(0, len(data_file_featureX)):
            X[data_file_featureX[i]] = robjects.FloatVector(data[data_file_featureX[i]])
        data_featureX = robjects.DataFrame(X)


        data_featureY = robjects.DataFrame({
            data_file_featureY: robjects.FloatVector(data[data_file_featureY])
        })
        result = []

        #线性回归
        if data_file_method == '1':
            result = def_lm(data_featureX, data_featureY, data_file_alternative)

        #多项式回归
        if data_file_method == '2':
            result = def_PolReg(data_featureX, data_featureY, eval(data_file_parameterMax), data_file_alternative)

        #逻辑回归
        if data_file_method == '3':
            result = def_logit(data_featureX, data_featureY, data_file_alternative)

        #非线性回归
        if data_file_method == '4':
            formula = robjects.Formula(data_file_nonLinearFunction)
            data_file_numberFormName.remove('')
            data_file_numberFormValue.remove('')
            start = {}
            for index, value in zip(data_file_numberFormName, data_file_numberFormValue):
                start[index] = value
            start = robjects.ListVector(start)
            result = def_nonlinear(data_featureX, data_featureY, formula, start)
            if '---' in str(result):
                result_1Coefficients_data = list(
                    filter(None, str(result).split('Parameters:')[1].split('---')[0].split('\n\r\n')))
                del result_1Coefficients_data[0]
                result_1Coefficients_datas = []
                for i in range(0, len(result_1Coefficients_data)):
                    Coefficients_row = list(filter(None, result_1Coefficients_data[i].split(' ')))
                    if len(Coefficients_row) == 6:
                        del Coefficients_row[-1]
                    result_1Coefficients_datas.append(Coefficients_row)
            else:
                result_1Coefficients_data = list(
                    filter(None, str(result).split('Parameters:')[1].split('Residual standard error:')[0].split(
                        '\n\r\n')))
                del result_1Coefficients_data[0]
                result_1Coefficients_datas = []
                for i in range(0, len(result_1Coefficients_data)):
                    result_1Coefficients_datas.append(list(filter(None, result_1Coefficients_data[i].split(' '))))
            [result_1Coefficients_cols_final, result_1Coefficients] = coefficients_datas_to_dict(
                result_1Coefficients_datas)
            result_nonLinear1 = \
                str(result).split('Residual standard error:')[1].split('Number of iterations to convergence:')[0].split(
                 '\n\r\n')
            result_nonLinear1 = 'Residual standard error:' + result_nonLinear1[0]
            result_nonLinear2 = str(result).split('Number of iterations to convergence:')[1].split('Achieved')[0].split(
                '\n\r\n')
            result_nonLinear2 = 'Number of iterations to convergence:' + result_nonLinear2[0]
            result_nonLinear3 = 'Achieved convergence tolerance:' + str(result).split('Achieved convergence tolerance:'
                                                                                      )[1].split('\n\r\n')[0]
            result_nonLinear = pd.DataFrame([result_nonLinear1, result_nonLinear2, result_nonLinear3], columns=['Model Summary'])
            result_nonLinear_cols = ['Model Summary']
            result_nonLinear = result_nonLinear.to_dict(orient='records')

        if result and data_file_method != '4':
            result_1residual = list(
                filter(None, str(result[0]).split('Residuals:')[1].split('Coefficients:')[0].split('\n\r\n')))
            result_1residual_cols = list(filter(None, result_1residual[0].split(' ')))
            result_1residual_data = list(filter(None, result_1residual[1].split(' ')))
            result_1residuals = pd.DataFrame(result_1residual_data, index=result_1residual_cols, dtype='float').T
            result_1residuals = result_1residuals.to_dict(orient='records')

            if '---' in str(result[0]):
                result_1Coefficients_data = list(
                    filter(None, str(result[0]).split('Coefficients:')[1].split('---')[0].split('\n\r\n')))
                del result_1Coefficients_data[0]
                result_1Coefficients_datas = []
                for i in range(0, len(result_1Coefficients_data)):
                    Coefficients_row = list(filter(None, result_1Coefficients_data[i].split(' ')))
                    if len(Coefficients_row) == 6:
                        del Coefficients_row[-1]
                    result_1Coefficients_datas.append(Coefficients_row)
            else:
                result_1Coefficients_data = list(
                    filter(None, str(result[0]).split('Coefficients:')[1].split('Residual standard error:')[0].split(
                        '\n\r\n')))
                del result_1Coefficients_data[0]
                result_1Coefficients_datas = []
                for i in range(0, len(result_1Coefficients_data)):
                    result_1Coefficients_datas.append(list(filter(None, result_1Coefficients_data[i].split(' '))))
            [result_1Coefficients_cols_final, result_1Coefficients] = coefficients_datas_to_dict(
                result_1Coefficients_datas)

            result_1Error_res = str(result[0]).split('Residual standard error:')[1].split(
                'degrees of freedom')[0].split('\n\r\n')[0].split('on')[0]
            result_1Error_df = str(result[0]).split('Residual standard error:')[1].split(
                'degrees of freedom')[0].split('\n\r\n')[0].split('on')[1]
            result_1_summary = pd.DataFrame([result_1Error_res, result_1Error_df], index=['Residual standard error',
                                                                                          'df'], dtype=float).T
            if 'Multiple R-squared:' in str(result[0]):
                result_1Mutiple_R2 = float(str(result[0]).split('Multiple R-squared:')[1].split(
                    'Adjusted R-squared:')[0].split(',')[0])
                result_1Adjusted_R2 = float(str(result[0]).split('Adjusted R-squared:')[1].split(
                    'F-statistic:')[0])
                result_1_summary['R-squared:'] = [result_1Mutiple_R2]
                result_1_summary['Adjusted R-squared:'] = [result_1Adjusted_R2]
            if 'F-statistic:' in str(result[0]):
                result_1Fstatistic = str(result[0]).split('F-statistic:')[1].split('on')[0].split(',')[0]
                result_1Pvalues = str(result[0]).split('p-value:')[1]
                result_1_summary['F-statistic:'] = [result_1Fstatistic]
                result_1_summary['p-value:'] = [result_1Pvalues]
            result_1_summary_cols = list(result_1_summary.columns)
            result_1_summary = result_1_summary.to_dict(orient='records')

            result_2datas = []
            result_2cols = ['result2', '2.5%', '97.5%']
            result_2drows = str(result[1]).split('\n\r\n')[1:]
            for i in range(0, len(result_2drows)):
                result_2datas.append(list(filter(None, result_2drows[i].split(' '))))
            result_2 = pd.DataFrame(result_2datas, columns=result_2cols)
            result_2 = result_2.drop([0], axis=0)
            result_2 = result_2.to_dict(orient='records')
            result_2cols_final = []
            for col in result_2cols:
                col_final = {"prop": col.replace('.', ''), 'label': col}
                result_2cols_final.append(col_final)
            for row in result_2:
                for col in result_2cols:
                    row[col.replace('.', '')] = row[col]

            result_34 = pd.DataFrame([list(data[data_file_featureY]), list(result[2]), list(result[3])],
                                     index=['真实值', '拟合值', '残差'], dtype=float).T
            result_34 = result_34.applymap("{0:.04f}".format)
            result_34cols = list(result_34.columns)
            result_34 = result_34.to_dict(orient='records')

            data_rows = data.shape[0]
            plt.scatter(range(1, data_rows+1), list(result[3]))
            file_name = 'residual_plot'+str(time.time())+'.png'
            curPath = os.path.abspath(os.path.dirname(__file__))
            rootPath = curPath[:curPath.find("dataanalysisplatform\\") + len("dataanalysisplatform\\")]
            pltsave_rootPath = rootPath.replace('\\', '/')
            plt.savefig(pltsave_rootPath+'app/static/PythonPlot/'+file_name)
            result_34_plot = ['\\static\\PythonPlot\\'+file_name]
            plt.close()

            if '无法计算VIF' not in str(result[4]):
                result_5cols = list(filter(None, str(result[4]).split('\n\r\n')[0].split(' ')))
                result_5datas = list(filter(None, str(result[4]).split('\n\r\n')[1].split('\n')[0].split(' ')))
                result_5 = pd.DataFrame(result_5datas, index=result_5cols, dtype=float).T
                result_5 = result_5.to_dict(orient='records')
            else:
                result_5cols = ['msg']
                result_5 = [{'msg': '模型中仅剩下一个变量，无法计算VIF'}]

            result_6chisquare = float(str(result[5]).split('Chisquare = ')[1].split(', Df = ')[0])
            result_6Df = float(str(result[5]).split('Chisquare = ')[1].split(', Df = ')[1].split(', p = ')[0])
            result_6Pvalue = float(str(result[5]).split('Chisquare = ')[1].split(', Df = ')[1].split(', p = ')[1])
            result_6cols = ['Chisquare', 'Df', 'p']
            result_6 = pd.DataFrame([[result_6chisquare, result_6Df, result_6Pvalue]], columns=result_6cols)
            result_6 = result_6.to_dict(orient='records')

            result_7 = []
            result_7cols = ['lag', 'Autocorrelation', 'D-W Statistic', 'p-value']
            result_7datas = list(
                filter(not_empty, str(result[6]).split('p-value')[1].split('Alternative')[0].split('\n\r\n')))
            for i in range(0, len(result_7datas)):
                result_7.append([float(x) for x in list(filter(None, result_7datas[i].split(' ')))])
            result_7 = pd.DataFrame(result_7, columns=result_7cols)
            result_7 = result_7.to_dict(orient='records')

            result_8 = []
            result_8cols = ['rstudent', 'unadjusted p-value', 'Bonferonni', 'p']
            result_8datas = list(filter(None, str(result[7]).split('p-value Bonferonni p')[1].split('\n\r\n')))
            for i in range(0, len(result_8datas)):
                result_8.append(list(filter(None, result_8datas[i].split(' '))))
            result_8 = pd.DataFrame(result_8, columns=result_8cols, dtype=float)
            result_8 = result_8.to_dict(orient='records')

    res = {'status': 1, 'result_1residual_cols': result_1residual_cols, 'result_1residuals': result_1residuals,
           'result_1Coefficients_cols': result_1Coefficients_cols_final, 'result_1Coefficients': result_1Coefficients,
           'result_1_summary_cols': result_1_summary_cols, 'result_1_summary': result_1_summary, 'result_2cols':
           result_2cols_final, 'result_2': result_2, 'result_34cols': result_34cols, 'result_34': result_34,
           'result_34_plot': result_34_plot,  'result_5cols': result_5cols, 'result_5': result_5, 'result_6cols':
           result_6cols, 'result_6': result_6, 'result_7cols': result_7cols, 'result_7': result_7, 'result_8cols':
           result_8cols, 'result_8': result_8, 'result_nonLinear_cols': result_nonLinear_cols, 'result_nonLinear':
           result_nonLinear}

    return jsonify(res)

#
def not_empty(s):
    return s and s.strip()

#
def coefficients_datas_to_dict(result_1Coefficients_datas):
    result_1Coefficients_cols = ['Coefficients:', 'Estimate', 'Std.Error', 't value', 'Pr(>|t|)']
    result_1Coefficients_datas = judge_option(result_1Coefficients_datas)
    result_1Coefficients = pd.DataFrame(result_1Coefficients_datas, columns=result_1Coefficients_cols, dtype=float)
    result_1Coefficients = result_1Coefficients.to_dict(orient='records')
    result_1Coefficients_cols_final = []
    for col in result_1Coefficients_cols:
        col_final = {"prop": col.replace('.', ''), 'label': col}
        result_1Coefficients_cols_final.append(col_final)
    for row in result_1Coefficients:
        for col in result_1Coefficients_cols:
            row[col.replace('.', '')] = row[col]

    return result_1Coefficients_cols_final, result_1Coefficients

#
def judge_option(result_1Coefficients_datas):
    for item in result_1Coefficients_datas:
        if '<' in item:
            index_of_sign = item.index('<')
            item[index_of_sign] = item[index_of_sign] + item[index_of_sign + 1]
            item.pop(index_of_sign + 1)
            item.pop(-1)

    return result_1Coefficients_datas
