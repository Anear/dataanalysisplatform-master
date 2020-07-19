# _*_ coding: UTF-8 _*_

__author__ = 'zhangchao'

from flask import Blueprint

home = Blueprint('home', __name__)

import app.home.views
