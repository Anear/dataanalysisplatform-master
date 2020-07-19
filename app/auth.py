# _*_ coding: UTF-8 _*_
from functools import wraps

from bson import ObjectId
from flask import session, url_for, redirect, request, abort

from app import mongo

__author__ = 'zhangchao'


# 登录装饰器
def login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 权限控制装饰器
def auth_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            if request.method == 'POST':
                abort(401)
            return redirect(url_for("home.login", next=request.url))
        user = mongo.db.user.find_one({'_id': ObjectId(session['user_id'])})
        # 查询所有角色ID
        role_ids = list(map(lambda v: ObjectId(v), user.get('roles', [])))
        roles = list(mongo.db.role.find({'_id': {'$in': role_ids}}, {'resources': 1}))
        role_resource_ids = []
        # 查询所有资源ID
        for role in roles:
            role_resource_ids.extend(role.get('resources', []))
        resource_ids = list(map(lambda v:ObjectId(v), list(set(role_resource_ids))))

        urls = []
        if resource_ids:
            resources = list(mongo.db.resource.find({'_id': {'$in': resource_ids}}, {'url': 1}))
            for resource in resources:
                if resource['url']:
                    urls.append(resource['url'])
        rule = request.url_rule
        if str(rule) not in urls:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
