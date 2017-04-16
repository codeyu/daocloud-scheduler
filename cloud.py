# coding: utf-8
import os
import json
import requests
import leancloud
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
    requests.packages.urllib3.disable_warnings()
    result = requests.get('https://openapi.daocloud.io/v1/apps', headers={"Authorization": "token " + DAOCLOUD_APITOKEN})
    data = json.loads(result.text)
    DaoCloudApp = Object.extend('DaoCloudApp')
    query = leancloud.Query('DaoCloudApp')
    for daoapp in data['app']:
        query.equal_to("appid", daoapp['id'])
        try:
            dao = query.first()
            dao.set('state', daoapp['state'])
            dao.set('last_operated_at', daoapp['last_operated_at'])
            dao.save()
        except leancloud.LeanCloudError as e:
            if e.code == 101:
                dao = DaoCloudApp()
                dao.set('appid', daoapp['id'])
                dao.set('name', daoapp['name'])
                dao.set('state', daoapp['state'])
                dao.set('last_operated_at', daoapp['last_operated_at'])
                dao.save()
            else:
                raise e
    return result.text
