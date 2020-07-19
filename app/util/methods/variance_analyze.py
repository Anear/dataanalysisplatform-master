# _*_ coding: UTF-8 _*_

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

#单因素分析
def aov_oneway(X, Y):
    namelist_X = X.columns.values.tolist()
    name_Y = Y.columns.values.tolist()[0]
    data = X
    data[name_Y] = Y

    name_X1 = namelist_X[0]
    fomula = name_Y + ' ~ ' + name_X1
    model = anova_lm(ols(fomula, data).fit())

    return model

#双因素分析
def aov_twoway(X, Y):
    namelist_X = X.columns.values.tolist()
    name_Y = Y.columns.values.tolist()[0]
    data = X
    data[name_Y] = Y

    name_X1 = namelist_X[0]
    name_X2 = namelist_X[1]
    fomula = name_Y + ' ~ ' + name_X1 + ' + ' + name_X2
    model = anova_lm(ols(fomula, data).fit())

    return model

#多因素分析
def aov_twoway_cross(X, Y):
    namelist_X = X.columns.values.tolist()
    name_Y = Y.columns.values.tolist()[0]
    data = X
    data[name_Y] = Y

    name_X1 = namelist_X[0]
    name_X2 = namelist_X[1]
    fomula = name_Y + ' ~ ' + name_X1 + ' * ' + name_X2
    model = anova_lm(ols(fomula, data).fit())

    return model


def aov_multiway(X, Y):
    namelist_X = X.columns.values.tolist()
    name_Y = Y.columns.values.tolist()[0]
    data = X
    data[name_Y] = Y

    length = len(namelist_X)
    fomula = name_Y + ' ~ '
    for i in range(length):
        fomula = fomula + '+' + namelist_X[i]
    model = anova_lm(ols(fomula, data).fit())

    return model


def aov_multiway_cross(X, Y, *args):
    namelist_X = X.columns.values.tolist()
    name_Y = Y.columns.values.tolist()[0]
    data = X
    data[name_Y] = Y

    str = ''
    for values in args:
        str += '+' + values

    length = len(namelist_X)
    fomula = name_Y + ' ~ ' + namelist_X[0]
    for i in range(1, length):
        fomula += '+' + namelist_X[i]
    fomula += str
    model = anova_lm(ols(fomula, data).fit())

    return model
