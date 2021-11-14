import json
import uuid

from flask import request, Response
from flask_socketio import *

import service
from settings import *

# SocketIO
socket_io = SocketIO(app, cors_allowed_origins="*")

valid_object = ["author", "origin", "conversationId", "data"]


def validate_request_object(request_object):
    return all(key in request_object for key in valid_object)


@app.route("/v1/ping")
def ping():
    response = {"ok": True, "msg ": "pong"}
    return Response(json.dumps(response), status=200, mimetype='application/json')


@app.route("/v1/info")
def info():
    response = {"ok": True,
                "author ": {
                    "author": "Sachin Sharma", "email": "sachinsharma31261@gmail.com"
                },
                "frontend": {

                }, "language": "javacript| python",
                "sources": "https://github.com/sachinsharma3191/ava_full_stack_app"}

    return Response(json.dumps(response), status=200, mimetype='application/json')


@app.route("/v1/conversations")
def get_conversations():
    conversations = service.get_all_conversations()
    if len(conversations) == 0:
        response = {"ok": True, "msg": "Unable to fetch conversations"}
        return Response(json.dumps(response), status=400, mimetype='application/json')

    response = {"ok": True, "conversations": conversations}
    return Response(json.dumps(response), status=400, mimetype='application/json')


@app.route("/v1/mutate", methods=["POST"])
def mutate_conversations():
    response = {"ok": True, "text": "Conversation Saved"}

    json_request = request.get_json()

    response['text'] = json_request['data']['text']
    json_request["message_id"] = str(uuid.uuid4())

    if not validate_request_object(json_request):
        error = {"ok": False, "msg": "Please provide all the fields in request body"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    resp = service.insert_conversation(json_request)
    if not resp:
        error = {"ok": False, "msg": "Unable to save the conversation"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    return Response(json.dumps(response), status=201, mimetype='application/json')


@app.route('/v1/delete', methods=["POST"])
def delete_conversations():
    response = {"ok": True, "text": "Conversation Deleted"}
    json_request = request.get_json()

    resp = service.delete_conversation(json_request)
    if not resp:
        error = {"ok": False, "msg": "Unable to delete conversation"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    return Response(json.dumps(response), status=200, mimetype='application/json')


@app.route('/v1/conversation/star', methods=["POST"])
def star_conversation():
    response = {"ok": True, "text": "Conversation Starred"}
    json_request = request.get_json()
    resp = service.star_conversation(json_request)
    if not resp:
        error = {"ok": False, "msg": "Unable to star the conversation"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    return Response(json.dumps(response), status=200, mimetype='application/json')


@app.route('/v1/conversation/unstar', methods=["POST"])
def Unstar_conversation():
    response = {"ok": True, "text": "Conversation Unstarred"}
    json_request = request.get_json()
    resp = service.unstar_conversation(json_request)
    if not resp:
        error = {"ok": False, "msg": "Unable to star the conversation"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    return Response(json.dumps(response), status=200, mimetype='application/json')


# SocketIO Events
@socket_io.on('connect')
def connected():
    print('Connected')


@socket_io.on('disconnect')
def disconnected():
    print('Disconnected')


if __name__ == '__main__':
    socket_io.run(app, port=5060, debug=True)
