import string
import random
import json
import uuid
from time import sleep

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

from impl.ClientQueueServiceImpl import ClientQueueServiceImpl
from impl.environment import Environment
from impl.logger import Logger
from impl.mongo import Mongo

app = Flask(__name__)
cors = CORS(app)

config = Environment()
db = Mongo(
    config.db_hostname,
    port=config.db_port,
    username=config.db_username,
    password=config.db_password,
    dbname=config.db_name)

logger = Logger.get_logger()

letters = string.ascii_lowercase

uuid_mq = None


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/info', methods=['GET', 'POST'])
def get_db_info():
    if not db.is_up():
        db.connect()

    info = str(db.info())
    print(info)
    resp = jsonify({'info': info})
    resp.status_code = 200
    return resp


@app.route('/random', methods=['GET', 'POST'])
def get_random_string():
    value = str(''.join(random.choice(letters) for i in range(10)))
    db.insert("string", {'value': value})
    resp = jsonify({'random_string': value})
    resp.status_code = 200
    return resp


@app.route('/randoms', methods=['GET', 'POST'])
def get_randoms_string():
    response = jsonify()
    response.status_code = 200
    response = jsonify(randoms_string=db.fetch_all("string"))
    return response


@app.route('/uuid', methods=['GET', 'POST'])
def get_random_uuid():
    value = str(uuid_mq.get_response(body=str(uuid.uuid4())))
    db.insert("uuid", {'value': value})
    resp = jsonify({'uuid': value})
    resp.status_code = 200
    return resp


@app.route('/uuids', methods=['GET', 'POST'])
def get_uuids():
    response = jsonify()
    response.status_code = 200
    response = jsonify(uuids=db.fetch_all("uuid"))
    return response


def retry(func):
    for i in range(0, 5):
        while True:
            try:
                return func()
            except Exception:
                sleep(3)
                continue
            break


if __name__ == '__main__':
    sleep(5)
    db.connect()
    uuid_mq = ClientQueueServiceImpl(config.rb_username, config.rb_password, config.rb_hostname, config.rb_port, 'hello_word')
    app.run(host='0.0.0.0', debug=True)
