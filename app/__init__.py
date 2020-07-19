# _*_ coding: UTF-8 _*_
import datetime

import redis as redis
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from flask_session import Session

__author__ = 'zhangchao'


app = Flask(__name__)

#配置mongo数据库
app.config['MONGO_URI'] = 'mongodb://172.19.235.128:27017/statistic_engine'

#设置的安全码
app.config['SECRET_KEY'] = 'you do not know'

#session存储格式为redis
app.config['SESSION_TYPE'] = 'redis'

# 设置redis的ip,port
app.config['SESSION_REDIS'] = redis.Redis(host='172.19.235.133', port=6379)

#
app.config['SESSION_KEY_PREFIX'] = 'flask'

#
app.config['SESSION_USE_SIGNER'] = True

#开启debug模式
app.debug = True

#热更新html模板
app.jinja_env.auto_reload = True

#配置数据库随app启动
mongo = PyMongo(app)
Session(app)

from app.home import home as home_blueprint
from app.service import service as service_blueprint
from app.system_manage import system_manage as system_manage_blueprint
from app.import_description import import_description as import_description_blueprint

from app.basic_test import basic_test as basic_test_blueprint
from app.variance_analyze import variance_analyze as variance_analyze_blueprint
from app.time_series import time_series as time_series_blueprint
from app.category_analyze import category_analyze as category_analyze_blueprint
from app.component_factor_analyze import component_factor_analyze as component_factor_blueprint
from app.regression_analyze import regression_analyze as regression_analyze_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(service_blueprint)
app.register_blueprint(system_manage_blueprint)
#这行有时报错
app.register_blueprint(import_description_blueprint)
app.register_blueprint(basic_test_blueprint)
app.register_blueprint(component_factor_blueprint)
app.register_blueprint(category_analyze_blueprint)
app.register_blueprint(time_series_blueprint)
app.register_blueprint(variance_analyze_blueprint)
app.register_blueprint(regression_analyze_blueprint)

app.permanent_session_lifetime = datetime.timedelta(days=10)


# 需登录
@app.errorhandler(401)
def no_login(error):
    if request.method == 'POST':
        return jsonify({'status': 0, 'err_code': 401, 'msg': '登录失效，请重新登录'})
    return redirect(url_for("home.login", next=request.url))


# 无权限
@app.errorhandler(403)
def no_auth(error):
    if request.method == 'POST':
        return jsonify({'status': 0, 'err_code': 403, 'msg': '无权访问', 'next': request.url})
    return render_template("403.html"), 403


# 找不到
@app.errorhandler(404)
def page_not_found(error):
    if request.method == 'POST':
        return jsonify({'status': 0, 'err_code': 404, 'msg': '找不到此路径', 'next': request.url})
    return render_template("404.html"), 404



