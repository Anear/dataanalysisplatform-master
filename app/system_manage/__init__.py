# _*_ coding: UTF-8 _*_

__author__ = 'zhangchao'

from flask import Blueprint

system_manage = Blueprint('system_manage', __name__)

import app.system_manage.menu_views
import app.system_manage.resource_views
import app.system_manage.role_views
import app.system_manage.user_views
