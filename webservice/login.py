import json
import dbmodels
import util
import base64
import boto3
import util2


def login(body):
    parameters = ["username", "password", "audio"]
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

    if not user:
        return 404, json.dumps({
            "code": 404,
            "message": "User not found"
        })

    password = body.get('password', "-----")
    if user.password != password:
        return 401, json.dumps({
            "code": 401,
            "message": "Incorrect credentials"
        })

    saved_features = user.audio
    audio = body['audio']
    audio = base64.b64decode(audio)
    fname = './tmp/' + util.random_string(20)
    with open(fname, 'wb') as f:
        f.write(audio)

    test_features = util2.features_dict(fname)

    record = {}
    for feat in util2.features_names:
        record[feat] = abs(saved_features[feat] - test_features[feat])
        mean = util2.zmean[feat]['mean']
        stdev = util2.zmean[feat]['stdev']
        record[feat] = str((record[feat] - mean)/stdev)
    record['id'] = '1'
    print(record)

    client = boto3.client('machinelearning')
    response = client.predict(MLModelId="ml-2EYiaqUQDVw", Record=record, PredictEndpoint="https://realtime.machinelearning.us-east-1.amazonaws.com")
    ans = response['Prediction']['predictedLabel']

    if ans == "0":
        return 401, json.dumps({
            "code": 401,
            "message": "Biometric authentication failed."
        })

    return 200, json.dumps({
        "code": 200,
        "message": "OK"
    })
