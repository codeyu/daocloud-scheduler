# coding: utf-8

from datetime import datetime

from flask import Flask
from flask import render_template
from flask_sockets import Sockets
from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
app = Flask(__name__)
sockets = Sockets(app)

class DaoCloudApp(Object):
    pass

@app.route('/')
def index():
    try:
        apps = Query(DaoCloudApp).descending('createdAt').find()
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            apps = []
        else:
            raise e
    return render_template('index.html', apps=apps)


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
