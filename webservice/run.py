#!/usr/bin/env python

import dotenv
from bottle import route, run, post, error, request, response
import bottle
import os
import register
import login
import json
import logging


bottle.BaseRequest.MEMFILE_MAX = (5<<20)

dotenv.load_dotenv()


@post('/register')
def do_register():
    logging.debug(str(request.json))
    try:
        resp_code, resp = register.register(request.json)
    except Exception as e:
        resp_code, resp = 500, json.dumps({
            "code": 500,
            "message": "Error.",
            "error": str(e)
        })

    response.status = resp_code
    return resp


@post('/login')
def do_login():
    logging.debug(request.json)
    try:
        resp_code, resp = login.login(request.json)
    except Exception as e:
        resp_code, resp = 500, json.dumps({
            "code": 500,
            "message": "Error.",
            "error": str(e)
        })
    response.status = resp_code
    return resp


@error(404)
def index(error):
    return json.dumps({
        "code": 200,
        "message": "Hello World"
    })


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get('HOST', 'localhost')
    run(host=host, port=port, debug=True)
