# _*_ coding: UTF-8 _*_
from bson import ObjectId
from flask import render_template, request, jsonify

from app import mongo
from app.auth import auth_req
from . import system_manage

__author__ = 'zhangchao'


# 角色管理
@system_manage.route('/system/role/')
def role_manage():
    return render_template('system_manage/roles.html', name='role_manage')


# 分页查询资源
@system_manage.route('/system/role/roles/', methods=['POST'])
def find_roles():
    name = request.values.get('name')
    page_num = int(request.values.get('pageNum', '1'))
    query = {}
    if name:
        query = {'name': '/' + name + '/'}
    roles = mongo.db.role.find(query).skip((page_num - 1) * 20).limit(20)
    total = roles.count()
    data = list(roles)
    for role in data:
        role['_id'] = str(role['_id'])
    return jsonify({
        'status': 1,
        'data': data,
        'total': total
    })


# 添加角色
@system_manage.route('/system/role/add/', methods=['POST'])
@auth_req
def add_role():
    name = request.values.get('name')
    key = request.values.get('key')
    mongo.db.role.insert({'name': name, 'key': key})
    return jsonify({'status': 1})


# 删除角色
@system_manage.route('/system/role/del/', methods=['POST'])
def del_role():
    _id = request.values.get('_id')
    mongo.db.role.delete_one({'_id': ObjectId(_id)})
    # todo 同时删除用户角色相关关联
    return jsonify({'status': 1})


# 修改角色
@system_manage.route('/system/role/edit/', methods=['POST'])
def edit_role():
    _id = request.values.get('_id')
    name = request.values.get('name')
    key = request.values.get('key')
    mongo.db.role.update({'_id': ObjectId(_id)}, {'$set': {'name': name, 'key': key}})
    return jsonify({'status': 1})


# 编辑角色资源
@system_manage.route('/system/role/resource/edit/', methods=['POST'])
def edit_role_resource():
    _id = request.values.get('_id')
    resources = request.values.getlist('resources[]')
    mongo.db.role.update({'_id': ObjectId(_id)}, {'$set': {'resources': resources}})
    return jsonify({'status': 1})


# 编辑角色菜单
@system_manage.route('/system/role/menu/edit/', methods=['POST'])
def edit_role_menu():
    _id = request.values.get('_id')
    menus = request.values.getlist('menus[]')
    mongo.db.role.update({'_id': ObjectId(_id)}, {'$set': {'menus': menus}})
    return jsonify({'status': 1})

