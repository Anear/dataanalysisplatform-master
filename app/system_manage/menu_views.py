# _*_ coding: UTF-8 _*_
import pymongo
from bson import ObjectId

from flask import render_template, request, jsonify

from app import mongo
from . import system_manage
from app.auth import login_req, auth_req

__author__ = 'zhangchao'


# 菜单管理
@system_manage.route('/system/menu/')
# @auth_req
def menu_manage():
    return render_template('system_manage/menus.html', name='menu_manage')


# 查询所有菜单
@system_manage.route('/system/menu/menus/', methods=['POST'])
def find_menus():
    name = request.values.get('name')
    parent_id = request.values.getlist('parentId[]')
    page_num = int(request.values.get('pageNum', '1'))
    query = {}
    if name:
        query = {'name': '/' + name + '/'}
    if parent_id != []:
        query['parent_id'] = parent_id[-1]
    sort_fields = [("parent_id", pymongo.ASCENDING), ("order", pymongo.ASCENDING)]
    menus = mongo.db.menu.find(query).sort(sort_fields).skip((page_num - 1) * 20).limit(20)
    total = menus.count()
    data = list(menus)
    for menu in data:
        menu['_id'] = str(menu['_id'])

    return jsonify({
        'status': 1,
        'data': data,
        'total': total,
    })


# 获取所有菜单选项
@system_manage.route('/system/menu/options/', methods=['POST'])
def find_menu_options():
    menus = mongo.db.menu.find({}, {'_id': 1, 'name': 1, 'parent_id': 1, 'type': 1})
    data = list(menus)
    for menu in data:
        menu['_id'] = str(menu['_id'])

    data_tree = []
    data_linear = data

    for i in data_linear:
        if i['parent_id'][-1] == '0':
            dict_list = {}
            dict_list['label'] = i['name']
            dict_list['value'] = i['_id']
            data_tree.append(to_tree_children(dict_list, data_linear))

    data.append({'_id': '0', 'name': '根目录'})

    return jsonify({
        'status': 1,
        'data': data,
        'data_tree': data_tree
    })


# 添加菜单
@system_manage.route('/system/menu/add/', methods=['POST'])
def add_menu():
    name = request.values.get('name')
    _type = request.values.get('type')
    parent_id = request.values.getlist('parentId[]')
    url = request.values.get('url', '')
    icon = request.values.get('icon', '')
    _order = request.values.get('order')
    menu = {'name': name, 'type': _type, 'parent_id': parent_id, 'url': url, 'icon': icon, 'order': _order}
    mongo.db.menu.insert(menu)
    return jsonify({'status': 1})


# 删除菜单
@system_manage.route('/system/menu/del/', methods=['POST'])
def del_menu():
    _id = request.values.get('_id')
    # 删除菜单
    mongo.db.menu.delete_one({'_id': ObjectId(_id)})
    # 删除子菜单
    mongo.db.menu.delete_many({'parent_id': _id})
    # 同时删除角色菜单相关关联
    mongo.db.role.update_many({'menus': _id}, {'$pull': {'menus': _id}})
    return jsonify({'status': 1})


# 修改菜单
@system_manage.route('/system/menu/edit/', methods=['POST'])
def edit_menu():
    _id = request.values.get('_id')
    name = request.values.get('name')
    parent_id = request.values.getlist('parentId[]')
    _type = request.values.get('type')
    url = request.values.get('url', '')
    _order = request.values.get('order')
    # 同一目录下重复性检查
    menu_brothers = mongo.db.menu.find({'_id': {'$nin': [ObjectId(_id)]}, 'parent_id': parent_id})
    for menu_brother in menu_brothers:
        if menu_brother.get('name') == name:
            return jsonify({'status': 0, 'msg': '同级目录不能重复'})
    update_sets = {'name': name, 'type': _type, 'parent_id': parent_id, 'url': url, 'order': _order}
    mongo.db.menu.update({'_id': ObjectId(_id)},
                         {'$set': update_sets})
    return jsonify({'status': 1})


# 修改菜单图标
@system_manage.route('/system/menu/icon/upd/', methods=['POST'])
def edit_menu_icon():
    _id = request.values.get('_id')
    icon = request.values.get('icon', '')
    mongo.db.menu.update({'_id': ObjectId(_id)}, {'$set': {'icon': icon}})
    return jsonify({'status': 1})


def to_tree_children(list, data_linear):
    for i in data_linear:
        if i['parent_id'][-1] == list['value']:
            dict_list = {}
            dict_list['label'] = i['name']
            dict_list['value'] = i['_id']
            if 'children' not in list:
                list['children'] = []
                list['children'].append(dict_list)
            else:
                list['children'].append(dict_list)

    if 'children' in list:
        for j in list['children']:
            to_tree_children(j, data_linear)

    return list