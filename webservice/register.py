import json
import base64
import util
import util2
import dbmodels


def register(body):
    parameters = ["username", "password", "audio", "email", "firstName", "lastName"]
    for par in parameters:
        if par not in body:
            return 400, json.dumps({
                "code": 400,
                "message": "Bad request. " + ",".join(parameters) + " parameters are required."
            })

    username = body['username']

    user = None
    for x in dbmodels.User.query(hash_key=username):
        user = x

    if user:
        return 409, json.dumps({
            "code": 409,
            "message": "Username already exists."
        }) 

    audio = body['audio']
    audio = base64.b64decode(audio)
    fname = './tmp/' + util.random_string(20)
    with open(fname, 'wb') as f:
        f.write(audio)

    features = util2.features_dict(fname)
    features = util2.normalize_feature(features)

    user = dbmodels.User(username=username,
                         email=body['email'],
                         password=body['password'],
                         firstName=body['firstName'],
                         lastName=body['lastName'],
                         audio=features)
    user.save()

    return 200, json.dumps({
        "code": 200,
        "message": "OK"
    })
