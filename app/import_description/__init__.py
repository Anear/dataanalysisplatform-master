# _*_ coding: UTF-8 _*_

__author__ = 'huyuxin'

from flask import Blueprint

import_description = Blueprint('import_description', __name__)

import app.import_description.views
