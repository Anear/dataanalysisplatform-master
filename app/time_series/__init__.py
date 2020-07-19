# _*_ coding: UTF-8 _*_

__author__ = 'huyuxin'

from flask import Blueprint
time_series = Blueprint('time_series', __name__)

import app.time_series.views