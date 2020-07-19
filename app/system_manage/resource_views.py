# _*_ coding: UTF-8 _*_

from bson import ObjectId

from flask import render_template, request, jsonify

from app import mongo
from app.auth import auth_req
from . import system_manage

__author__ = 'zhangchao'


# 资源管理
@system_manage.route('/system/resource/')
def resource_manage():
    return render_template('system_manage/resources.html', name='resource_manage')


# 分页查询资源
@system_manage.route('/system/resource/resources/', methods=['POST'])
def find_resources():
    name = request.values.get('name')
    page_num = int(request.values.get('pageNum'))
    query = {}
    if name:
        query = {'name': '/' + name + '/'}
    resources = mongo.db.resource.find(query).skip((page_num - 1) * 20).limit(20)
    total = resources.count()
    data = list(resources)
    for resource in data:
        resource['_id'] = str(resource['_id'])
    return jsonify({
        'status': 1,
        'data': data,
        'total': total
    })


# 添加资源
@system_manage.route('/system/resource/add/', methods=['POST'])
def add_resource():
    name = request.values.get('name')
    url = request.values.get('url')
    mongo.db.resource.insert({'name': name, 'url': url})
    return jsonify({'status': 1})


# 删除资源
@system_manage.route('/system/resource/del/', methods=['POST'])
def del_resource():
    _id = request.values.get('_id')
    mongo.db.resource.delete_one({'_id': ObjectId(_id)})
    # todo 同时删除角色资源相关关联
    return jsonify({'status': 1})


# 修改资源
@system_manage.route('/system/resource/edit/', methods=['POST'])
def edit_resource():
    _id = request.values.get('_id')
    name = request.values.get('name')
    url = request.values.get('url')
    mongo.db.resource.update({'_id': ObjectId(_id)}, {'$set': {'name': name, 'url': url}})
    return jsonify({'status': 1})
