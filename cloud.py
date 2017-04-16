# coding: utf-8
import os
import json
import requests

from leancloud import Engine
from leancloud import LeanEngineError
from leancloud import Object
from app import app

engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.define
def get_daocloud_app():
    DAOCLOUD_APITOKEN = os.environ.get('DAOCLOUD_APITOKEN')
    result = requests.get('https://openapi.daocloud.io/v1/apps', headers={"Authorization": "token " + DAOCLOUD_APITOKEN})
    data = json.loads(result.text)
    DaoCloudApp = Object.extend('DaoCloudApp')
    query = leancloud.Query('DaoCloudApp')
    for app in data['app']:
        query.equal_to("appid", app['id'])
        dao = query.first()
        if not dao:
            dao = DaoCloudApp()
            dao.set('appid', app['id'])
            dao.set('name', app['name'])
            dao.set('state', app['state'])
            dao.set('last_operated_at', app['last_operated_at'])
            dao.save()
        else:
            dao.set('state', app['state'])
            dao.set('last_operated_at', app['last_operated_at'])
            dao.save()
    return result.text
