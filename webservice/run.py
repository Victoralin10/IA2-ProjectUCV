#!/usr/bin/env python

import dotenv
from bottle import route, run, post, error, request, response
import bottle
import os
import register
import login


bottle.BaseRequest.MEMFILE_MAX = (5<<20)

dotenv.load_dotenv()


@post('/register')
def do_register():
    resp_code, resp = register.register(request.json)
    response.status = resp_code
    return resp


@post('/login')
def do_login():
    resp_code, resp = login.login(request.json)
    response.status = resp_code
    return resp


@error(404)
def index(error):
    return "Hello World"


port = int(os.environ.get("PORT", "8080"))
host = os.environ.get('HOST', 'localhost')
run(host=host, port=port, debug=True)