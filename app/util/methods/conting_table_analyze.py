# _*_ coding: UTF-8 _*_

from scipy.stats.stats import chisquare
import statsmodels.api as sm


def def_chisquare(f_obs1, f_exp1=None):
    res = chisquare(f_obs=f_obs1, f_exp=f_exp1, axis=None)
    return res


def def_table(table1):
    table = sm.stats.Table(table=table1, shift_zeros=True)
    rslt = table.test_nominal_association()
    df = rslt.df
    stat = rslt.statistic
    pvalue = rslt.pvalue
    orig = table.table_orig
    MarPro = table.marginal_probabilities
    return df, stat, pvalue, MarPro
