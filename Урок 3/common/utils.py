import json


def get_message(obj):
    encoded_response = obj.recv(1024)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(obj, message):
    dump_message = json.dumps(message)
    encoded_message = dump_message.encode('utf-8')
    obj.send(encoded_message)
