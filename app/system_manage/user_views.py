# _*_ coding: UTF-8 _*_
import pymongo
from bson import ObjectId

from flask import render_template, request, jsonify
from werkzeug.security import generate_password_hash

from app import mongo
from . import system_manage

__author__ = 'zhangchao'


# 跳转到用户管理页面
@system_manage.route('/system/user/')
def user_manage():
    return render_template('system_manage/users.html', name='user_manage')


# 查询所有用户
@system_manage.route('/system/user/users/', methods=['POST'])
def find_users():
    #取得用户名，页码
    username = request.values.get('username')
    page_num = int(request.values.get('pageNum'))
    query = {}
    if username:
        query = {'name': '/' + username + '/'}
    exclusive_cols = {'password': 0}
    sort_fields = [("_id", pymongo.ASCENDING)]
    #从数据库中取出用户信息，返回
    users = mongo.db.user.find(query, exclusive_cols).sort(sort_fields).skip((page_num - 1)*20).limit(20)
    total = users.count()
    data = list(users)
    for user in data:
        user['_id'] = str(user['_id'])

    return jsonify({
        'status': 1,
        'data': data,
        'total': total
    })


# 添加用户
@system_manage.route('/system/user/add/', methods=['POST'])
def add_user():
    # 重复性检查
    username = request.values.get('username')
    password = request.values.get('password')
    db_user = mongo.db.user.find_one({'username': username})
    if db_user:
        res = {'status': 0, 'msg': '用户名重复'}
    else:
        mongo.db.user.insert({'username': username, 'password': generate_password_hash(password), 'status': '0'})
        res = {'status': 1}
    return jsonify(res)


# 删除用户
@system_manage.route('/system/user/del/', methods=['POST'])
def del_user():
    _id = request.values.get('_id')
    # 删除用户
    mongo.db.user.delete_one({'_id': ObjectId(_id)})
    return jsonify({'status': 1})


# 编辑用户资料
@system_manage.route('/system/user/edit/', methods=['POST'])
def edit_user():
    # 根据用户id更新用户信息
    # 如果修改了用户名需要检查重复性
    _id = request.values.get('_id')
    username = request.values.get('username')
    mongo.db.user.update({'_id': ObjectId(_id)}, {'$set': {'username': username}})
    return jsonify({'status': 1})


# 编辑用户角色
@system_manage.route('/system/user/role/edit/', methods=['POST'])
def edit_user_role():
    _id = request.values.get('_id')
    roles = request.values.getlist('roles[]')
    mongo.db.user.update({'_id': ObjectId(_id)}, {'$set': {'roles': roles}})
    return jsonify({'status': 1})


# 编辑用户状态
@system_manage.route('/system/user/status/edit/', methods=['POST'])
def edit_user_status():
    _id = request.values.get('_id')
    status = request.values.get('status', '0')
    mongo.db.user.update({'_id': ObjectId(_id)}, {'$set': {'status': status}})
    return jsonify({'status': 1})


