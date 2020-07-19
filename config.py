# _*_ coding: UTF-8 _*_

import os

IMG_PATH = '/static/img/'
ROOT_PATH = os.path.dirname(__file__)
UPLOAD_PATH = os.path.join(ROOT_PATH, 'app/static/img/')

CHOOSE_METHOD_CONFIGS = {
    '1': {'col_name': '方差筛选字段', 'field_name': 'var_select', 'y_label': '方差'},
    '2': {'col_name': 'Kbest筛选字段', 'field_name': 'selectk_select', 'y_label': '卡方_Score'},
    '3': {'col_name': 'Tree筛选字段', 'field_name': 'tree_select', 'y_label': 'Decision_importance'},
}

ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv', 'txt'}

if __name__ == '__main__':
    print(UPLOAD_PATH)
    print(os.path.join(IMG_PATH, 'gh.png'))
