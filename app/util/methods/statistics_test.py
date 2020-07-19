# _*_ coding: UTF-8 _*_

from numpy import sqrt, mean, std
from scipy.stats.morestats import shapiro, bartlett, levene, fligner
from scipy.stats.stats import kstest, normaltest, kruskal
from scipy.stats import anderson, pearsonr, spearmanr, kendalltau, t, ttest_1samp, \
    ttest_ind, mannwhitneyu, ttest_rel, wilcoxon, f_oneway, friedmanchisquare
from statsmodels.sandbox.stats.runs import runstest_1samp
from scipy.stats.stats import chisquare
import statsmodels.api as sm

#皮尔森相关性系数
def def_pearsonr(x1, y1):
    #res = pearsonr(x=x1, y=y1)

    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for i in x1:
        if i in y1:
            n += 1
            x = x1[i]
            y = y1[i]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        res = (sum_xy - (sum_x * sum_y) / n) / denominator
        return res


#斯皮尔曼相关性系数
def def_spearman(a1):
    res = spearmanr(a=a1, axis=0, nan_policy='propagate')
    return res

#肯德尔相关性系数
def def_kendalltau(x1, y1):
    res = kendalltau(x=x1, y=y1, initial_lexsort=None, nan_policy='propagate', method='auto')
    return res


def def_ttest_1samp(a1, popmean1, alpha1=0.95):
    res = ttest_1samp(a=a1, popmean=popmean1)
    n = len(a1)
    df = n - 1
    stat = res.statistic[0]
    p_value = res.pvalue[0]
    mean_ = mean(a1) - popmean1
    sigma = std(a1, ddof=1)
    Lower, Upper = t.interval(alpha1, df, loc=mean_, scale=sigma / sqrt(n))
    Lower, Upper = Lower[0], Upper[0]
    return stat, df, p_value, mean_[0], Lower, Upper


def def_ttest_ind(a1, b1, var_is_equal=True, alpha1=0.95):
    res = ttest_ind(a=a1, b=b1, equal_var=var_is_equal)
    stat = res.statistic[0]
    p_value = res.pvalue[0]
    n1, n2 = len(a1), len(b1)
    mean_ = mean(a1) - mean(b1)
    s1 = float(std(a1, ddof=1))
    s2 = float(std(b1, ddof=1))
    if var_is_equal == True:
        df = n1 + n2 - 2
        s = sqrt(((n1 - 1) * (s1 ** 2) + (n2 - 1) * (s2 ** 2)) / (n1 + n2 - 2))
        scale = s * sqrt(1 / n1 + 1 / n2)
    else:
        df = (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2 / ((s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1))
        scale = sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    Lower, Upper = t.interval(alpha1, df, loc=mean_, scale=scale)

    return stat, df, p_value, mean_, Lower, Upper

#单样本T检验
def def_ttest_rel(a1, b1, alpha1=0.95):
    res = ttest_rel(a=a1, b=b1)
    stat = res.statistic[0]
    p_value = res.pvalue[0]
    c = a1.values - b1.values
    n = len(c)
    df = n - 1
    mean_ = mean(c)
    sigma = std(c, ddof=1)
    Lower, Upper = t.interval(alpha1, df, loc=mean_, scale=sigma / sqrt(n))
    return stat, df, p_value, mean_, Lower, Upper

#两独立样本T检验
def def_f_oneway(*args):
    res = f_oneway(*args)
    return res

#两配对样本T检验
def def_chisquare(f_obs1, f_exp1=None):
    res = chisquare(f_obs=f_obs1, f_exp=f_exp1, axis=None)
    return res


def def_table(table1):
    table = sm.stats.Table(table=table1, shift_zeros=True)
    rslt = table.test_nominal_association()
    df = rslt.df
    stat = rslt.statistic
    pvalue = rslt.pvalue
    MarPro = table.marginal_probabilities
    return df, stat, pvalue, MarPro

#曼—惠特尼U检验
def def_mannwhitneyu(x1, y1, use_continuity1=True, alternative1="two-sided"):
    res = mannwhitneyu(x=x1, y=y1, use_continuity=use_continuity1, alternative=alternative1)
    return res

#wilcoxon符号秩检验
def def_wilcoxon(x1, y1=None, correction1=False):
    res = wilcoxon(x=x1, y=y1, zero_method="wilcox", correction=correction1)
    return res

#克鲁什卡尔检验
def def_kruskal(*args):
    res = kruskal(*args)
    return res

#弗里德曼检验
def def_friedmanchisquare(*args):
    res = friedmanchisquare(*args)
    return res

#夏皮罗—威尔克检验
def def_shapiro(x1):
    res = shapiro(x=x1)
    return res

#正态分布检验
def def_normaltest(a1):
    res = normaltest(a=a1, nan_policy='propagate')
    return res

#安德森检验
def def_anderson(x1, dist1='norm'):
    res = anderson(x=x1, dist=dist1)
    return res

#KS检验
def def_kstest(rvs1, cdf1, args1=(), alternative1='two-sided'):
    res = kstest(rvs=rvs1, cdf=cdf1, args=args1, alternative=alternative1)
    return res

#巴特利检验
def def_bartlett(*args):
    res = bartlett(*args)
    return res

#levene检验
def def_levene(*args):
    res = levene(*args)
    return res

#fligner—Killen检验
def def_fligner(*args):
    res = fligner(*args)
    return res

#游程检验
def def_runstest(x1, cutoff1='mean', correction1=True):
    res = runstest_1samp(x=x1, cutoff=cutoff1, correction=correction1)
    return res
