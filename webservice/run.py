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

logger = logging.Logger("api")
handler = logging.FileHandler("app.log")
logger.addHandler(handler)
logger.setLevel(int(os.environ.get("LOG_LEVEL", "40")))


@post('/register')
def do_register():
    logger.debug(str(request.json))
    try:
        resp_code, resp = register.register(request.json)
    except Exception as ex:
        resp_code, resp = 500, json.dumps({
            "code": 500,
            "message": "Error.",
            "error": str(ex)
        })
        logger.error(ex, exc_info=True)

    response.status = resp_code
    return resp


@post('/login')
def do_login():
    logger.debug(request.json)
    try:
        resp_code, resp = login.login(request.json)
    except Exception as e:
        resp_code, resp = 500, json.dumps({
            "code": 500,
            "message": "Error.",
            "error": str(e)
        })
        logger.error(e, exc_info=True)

    response.status = resp_code
    return resp


@error(404)
def index(error):
    return json.dumps({
        "code": 200,
        "message": "Hello World"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get('HOST', 'localhost')
    run(host=host, port=port, debug=True)
