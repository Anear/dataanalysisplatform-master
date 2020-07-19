# _*_ coding: UTF-8 _*_

__author__ = 'zhangchao'

from flask import Blueprint

service = Blueprint('service', __name__)

import app.service.views