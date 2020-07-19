# _*_ coding: UTF-8 _*_

__author__ = 'huyuxin'

from flask import Blueprint
basic_test = Blueprint('basic_test', __name__)

import app.basic_test.views