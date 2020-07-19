# _*_ coding: UTF-8 _*_
import json
import pandas as pd

import pymongo
from bson import ObjectId

from flask import render_template, request, jsonify

from . import service
from app import mongo
from app.auth import login_req


@service.route('/main/spreadsheet/')
@login_req
def sheet_service_html():
    return render_template('service/sheet_manage.html', name='sheet_service_html')


@service.route('/main/operate/')
@login_req
def operate_html():
    return render_template('service/operate_manage.html', name='operate_service_html')


@service.route('/operate/init/', methods=['POST'])
@login_req
def find_scene():
    scenes = pd.DataFrame(list(mongo.db.scene.find({}, {'scene_name': 1, '_id': 0})))['scene_name']
    res = {'staus': 1, 'sceneCols': list(scenes)}
    return jsonify(res)

@service.route('/main/help/')
@login_req
def help_html():
    return render_template('service/Help.html', name='help_html')