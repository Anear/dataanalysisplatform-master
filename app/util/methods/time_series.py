# _*_ coding: UTF-8 _*_

import os
import time

from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt

from arch import arch_model
from statsmodels.tsa.seasonal import seasonal_decompose

#时序图
def def_plot(timeseries):
    #利用数据画图
    timeseries.plot()
    #为图命名
    file_name = 'ts_plot' + str(time.time()) + '.png'
    #获取当前文件的完整路径
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    #修改路径格式
    pltsave_rootPath = rootPath.replace('\\', '/')
    #将图片保存到系统目录
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    #关闭 window
    plt.close()
    #返回文件路径
    file_path = ['\\static\\PythonPlot\\' + file_name]
    return file_path

#ACF图
def def_acfplot(x1):
    plot_acf(x=x1)
    file_name = 'acf_plot' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    file_path = ['\\static\\PythonPlot\\'+file_name]
    plt.close()

    return file_path

#PACF图
def def_pacfplot(x1):
    plot_pacf(x=x1)

    file_name = 'pacf_plot' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    file_path = ['\\static\\PythonPlot\\'+file_name]
    plt.close()

    return file_path

#平稳性检验
def def_adfuller(x1, maxlag1=None, autolag1='AIC'):
    res = adfuller(x=x1, maxlag=maxlag1, autolag=autolag1)
    return res

#白噪声检验
def def_acorr_ljungbox(x1, lags1=None):
    res = acorr_ljungbox(x=x1, lags=lags1)
    return res

#AR模型
def def_AR(timeseries, p=1, steps1=1):
    model = ARIMA(timeseries, (p, 0, 0)).fit()
    summary = model.summary()
    forecast = model.forecast(steps=steps1)
    return summary, forecast

#MA模型
def def_MA(timeseries, q=1, steps1=1):
    model = ARIMA(timeseries, (0, 0, q)).fit()
    summary = model.summary()
    forecast = model.forecast(steps=steps1)
    return summary, forecast

#ARMA模型
def def_ARMA(timeseries, p=1, q=1, steps1=1):
    #fit( x, y, batch_size=32, epochs=10, verbose=1, callbacks=None,validation_split=0.0, validation_data=None,
    #shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0)
    model = ARIMA(timeseries, (p, 0, q)).fit()
    summary = model.summary()
    forecast = model.forecast(steps=steps1)
    return summary, forecast

#ARIMA模型
def def_ARIMA(timeseries, p, d, q, steps1):
    model = ARIMA(timeseries, (p, d, q)).fit()
    summary = model.summary()
    forecast = model.forecast(steps=steps1)
    return summary, forecast

#ARCH模型
def def_ARCH(y1, mean1='Constant', lags1=0, vol1='GARCH', p1=1, o1=0, q1=1, dist1='gaussian'):
    model = arch_model(y=y1, mean=mean1, lags=lags1, vol=vol1, p=p1, o=o1, q=q1, dist=dist1)
    fit = model.fit()
    summary = fit.summary()
    return summary

#季节分解模型
def def_decompose(x1, model1="additive"):
    res = seasonal_decompose(x=x1, model=model1, freq=12)
    trend = res.trend
    seasonal = res.seasonal
    resid = res.resid
    observed = res.observed
    res.plot()

    file_name = 'decompose_plot' + str(time.time()) + '.png'
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("dataanalysisplatform-master\\") + len("dataanalysisplatform-master\\")]
    pltsave_rootPath = rootPath.replace('\\', '/')
    plt.savefig(pltsave_rootPath + 'app/static/PythonPlot/' + file_name)
    file_path = ['\\static\\PythonPlot\\' + file_name]
    plt.close()

    return trend, seasonal, resid, observed, file_path
