# _*_ coding: UTF-8 _*_
# _*_ coding: UTF-8 _*_

import pymongo
from bson import ObjectId

from flask import render_template, redirect, url_for, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app import mongo
from . import home
from app.auth import login_req, auth_req

__author__ = 'zhangchao'

# 1.用户登录后系统首先生成菜单树
def generate_menu_tree(parent_id, data):
    children = []
    for menu in data:
        if menu['parent_id'][-1] != '0' and menu['parent_id'][-1] == parent_id:
            child = {'_id': menu['_id'], 'name': menu['name'], 'type': menu['type'], 'url': menu['url'],
                      'children': generate_menu_tree(menu['_id'], data)}
            children.append(child)
    return children


@home.route('/')
@login_req
def index():
    return render_template('import_description/description_analyze.html', name='index')


@home.route('/404')
def err_404():
    return render_template('404.html', name='err_404')


@home.route('/403')
def err_403():
    return render_template('403.html', name='err_403')




# 2.用户选择计算页面后，初始化用户菜单
@home.route("/user/menus/", methods=['POST'])
@auth_req
def init_user_menus():
    # 查询用户角色
    user_id = session['user_id']
    user = mongo.db.user.find_one({'_id': ObjectId(user_id)})
    role_ids = user.get('roles', [])
    user_menus = []
    # 根据用户-角色 查菜单
    if role_ids:
        role_id_objects = list(map(lambda v: ObjectId(v), role_ids))
        roles = list(mongo.db.role.find({'_id': {'$in': role_id_objects, '$exists': True}}, {'menus': 1}))
        menus_ids = []
        for role in roles:
            menus_ids.extend(list(map(lambda v:ObjectId(v), role.get('menus', []))))

        show_field = {'_id': 1, 'name': 1, 'parent_id': 1,  'type': 1, 'url': 1, 'icon': 1, 'order': 1}
        sort_list = [('parent_id', pymongo.ASCENDING), ('order', pymongo.ASCENDING)]
        menus = mongo.db.menu.find({'_id': {'$in': menus_ids}}, show_field).sort(sort_list)
        data = list(menus)
        for menu in data:
            menu['_id'] = str(menu['_id'])

        # 将数据组装好
        for menu in data:
            if menu['parent_id'][-1] == '0':
                data_item = {'_id': menu['_id'], 'name': menu['name'], 'type': menu['type'], 'url': menu['url'],
                             'icon': menu['icon'], 'children': generate_menu_tree(menu['_id'], data)}
                user_menus.append(data_item)

    return jsonify({
        'status': 1,
        'data': user_menus
    })


# 查询所有菜单
@home.route("/menus/", methods=['POST'])
def find_all_menus():
    show_field = {'_id': 1, 'name': 1, 'parent_id': 1,  'type': 1, 'url': 1, 'icon': 1, 'order': 1}
    sort_list = [('parent_id', pymongo.ASCENDING), ('order', pymongo.ASCENDING)]
    menus = mongo.db.menu.find({}, show_field).sort(sort_list)
    data = list(menus)
    for menu in data:
        menu['_id'] = str(menu['_id'])

    # 将数据组装好
    datas = []
    for menu in data:
        if menu['parent_id'][-1] == '0':
            data_item = {'_id': menu['_id'], 'name': menu['name'], 'type': menu['type'], 'url': menu['url'],
                         'icon': menu['icon'], 'children': generate_menu_tree(menu['_id'], data)}
            datas.append(data_item)

    return jsonify({
        'status': 1,
        'data': datas
    })


# 查询所有的资源
@home.route("/resources/", methods=['POST'])
def find_all_resources():
    resources = mongo.db.resource.find({}, {'_id': 1, 'name': 1})
    data = list(resources)
    for resource in data:
        resource['_id'] = str(resource['_id'])

    return jsonify({
        'status': 1,
        'data': data
    })


# 查询所有的角色
@home.route("/roles/", methods=['POST'])
def find_all_roles():
    roles = mongo.db.role.find({}, {'_id': 1, 'name': 1})
    data = list(roles)
    for role in data:
        role['_id'] = str(role['_id'])

    return jsonify({
        'status': 1,
        'data': data
    })


@home.route('/scenes/', methods=['POST'])
@login_req
def find_all_scenes():
    scenes = list(mongo.db.scene.find({}, {'scene_name': 1, '_id': 1}))
    for scene in scenes:
        scene['_id'] = str(scene['_id'])
        scene['sceneId'] = scene['_id']
        scene['sceneName'] = scene['scene_name']
    res = {'status': 1, 'scenes': scenes}
    return jsonify(res)

#######################################################################################################################
# 登录
@home.route("/login/", methods=["GET", "POST"])
def login():
    username = request.values.get('username', '')
    password = request.values.get('password', '')
    if request.method == 'POST':
        if username != '' or password != '':
            user = mongo.db.user.find_one({'username': username})
            if not check_password_hash(user['password'], password):
                return jsonify({'status': 0, 'msg': '密码错误'})
            # todo 将登录信息保存在redis中
            session.permanent = True
            session["user"] = user['username']
            session["user_id"] = str(user['_id'])
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'msg': '请输入账号和密码'})

    return render_template("login.html", name='login')


# 登出
@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 修改密码
@home.route("/password/reset/", methods=['GET', 'POST'])
@auth_req
def rest_password():
    if request.method == 'POST':

        password = request.values.get('password')
        new_password = request.values.get('newPassword')
        user_id = ObjectId(session.get('user_id'))
        user = mongo.db.user.find_one({'_id': user_id})
        if check_password_hash(user.get('password'), password):
            mongo.db.user.update({'_id': user_id}, {'$set': {'password': generate_password_hash(new_password)}})
            res = {'status': 1}
        else:
            res = {'status':0, 'msg': '原密码错误'}
        return jsonify(res)
    return render_template('reset_password.html', name='reset_password')
