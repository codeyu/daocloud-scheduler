# coding: utf-8

from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template


class DaoCloudApp(Object):
    pass

def show():
    try:
        apps = Query(DaoCloudApp).descending('createdAt').find()
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            apps = []
        else:
            raise e
    return render_template('index.html', apps=apps)

