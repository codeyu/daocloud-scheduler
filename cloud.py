# coding: utf-8
import os
import time
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
    print('get func begin run..')
    base_url = 'https://openapi.daocloud.io/v1/apps'
    DAOCLOUD_APITOKEN = os.environ.get('DAOCLOUD_APITOKEN')
    token = "token " + DAOCLOUD_APITOKEN
    requests.packages.urllib3.disable_warnings()
    result = requests.get(base_url, headers={"Authorization": token})
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
    print('get func OK')


@engine.define
def start_if_stop():
    print('start func begin run..')
    base_url = 'https://openapi.daocloud.io/v1/apps'
    DAOCLOUD_APITOKEN = os.environ.get('DAOCLOUD_APITOKEN')
    token = "token {token}".format(token=DAOCLOUD_APITOKEN)
    requests.packages.urllib3.disable_warnings()
    result = requests.get(base_url, headers={"Authorization": token})
    data = json.loads(result.text)
    DaoCloudApp = Object.extend('DaoCloudApp')
    query = leancloud.Query('DaoCloudApp')
    for daoapp in data['app']:
        try:
            if daoapp['state'] == 'stopped':
                action_id_text = requests.post(
                    '{0}/{1}/actions/start'.format(base_url, daoapp['id']),
                    headers={"Authorization": token}).text
                action_id = json.loads(action_id_text)
                action_result = 'IN_PROCESS'
                while action_result == 'IN_PROCESS':
                    action_result_text = requests.get(
                        '{0}/{1}/actions/{2}'.format(base_url,
                                                     daoapp['id'], action_id['action_id']),
                        headers={"Authorization": token}).text
                    action_result = json.loads(action_result_text)['state']
                    time.sleep(5)
                print(action_result)
        except leancloud.LeanCloudError as e:
            raise e
    print('start func OK')
