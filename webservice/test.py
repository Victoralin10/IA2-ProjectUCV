#!/usr/bin/env python

import dotenv
import requests
import os
import base64

dotenv.load_dotenv()

URL = "http://{host}:{port}".format(
    host=os.environ.get('HOST', 'localhost'),
    port=os.environ.get('PORT', '8080')
)
# URL = "https://0n31isnqy6.execute-api.us-east-1.amazonaws.com/prod/"

def test_register():
    with open('audio1.wav', "rb") as f:
        audio = base64.b64encode(f.read()).decode()

    user = {
        "username": "victoralin10",
        "password": "hola123",
        "email": "ingvcueva@gmail.com",
        "firstName": "Victor",
        "lastName": "Cueva",
        "audio": audio
    }
    resp = requests.post(URL+'/register', json=user)
    print(resp.text)


def test_login_positive():
    with open("audio2.wav", "rb") as f:
        audio = base64.b64encode(f.read()).decode()

    login = {
        "username": "victoralin10",
        "password": "hola123",
        "audio": audio
    }
    resp = requests.post(URL+'/login', json=login)
    print(resp.text)


def test_login_negative():
    with open("audio3.wav", "rb") as f:
        audio = base64.b64encode(f.read()).decode()

    login = {
        "username": "victoralin10",
        "password": "hola123",
        "audio": audio
    }
    resp = requests.post(URL+'/login', json=login)
    print(resp.text)


def main():
    print("Testing register")
    test_register()
    print("Testing positive authentication.")
    test_login_positive()
    print("Testing negative authentication.")
    test_login_negative()


if __name__ == "__main__":
    main()
