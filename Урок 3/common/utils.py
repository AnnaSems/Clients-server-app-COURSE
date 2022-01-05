import json


def get_message(obj):
    message_size = obj.recv(1024)
    if isinstance(message_size, bytes):
        json_response = message_size.decode('utf-8')
        response = json.loads(json_response)
        if type(response) == dict:
            return response
        raise ValueError
    raise ValueError


def send_message(obj, message):
    dump_message = json.dumps(message)
    encoded_message = dump_message.encode('utf-8')
    obj.send(encoded_message)
