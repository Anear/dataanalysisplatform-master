# _*_ coding: UTF-8 _*_

import pandas as pd
from numpy import mean, median, ptp, var, std, cov, corrcoef, percentile
from scipy.stats import mode, skew, kurtosis


def def_mode(a1):
    res = mode(a1, axis=0, nan_policy='omit')
    return res[0]


def def_median(a1):
    res = median(a1, axis=0)
    return res


def def_quantile(X, p):
    res = percentile(X, p, axis=0)
    return res


def def_mean(a1):
    res = mean(a1)
    return res


def def_ptp(a1):
    res = ptp(a1, axis=0)
    return res


def def_varBias(a1):
    res = cov(a1, bias=True)
    return res


def def_var(a1):
    res = cov(a1, bias=False)
    return res


def def_std(a1):
    res = std(a1)
    return res


def def_CV(a1):
    res = mean(a1) / std(a1)
    return res


def def_skew(a1, axis1=0):
    res = skew(a=a1, axis=axis1, nan_policy='omit')
    return res


def def_kurt(a1, axis1=0):
    res = kurtosis(a=a1, axis=axis1, nan_policy='omit')
    return res


def def_covBias(m1):
    res = cov(m=m1, bias=True)
    return res


def def_cov(m1):
    res = cov(m=m1, bias=False)
    return res


def def_corrcoef(x1, y1=None, bias1=True):
    res = corrcoef(x=x1, y=y1, bias=bias1)
    return res
