""" Функции клиента: сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777. """

from common.utils import get_message, send_message as s_m
from log.dec import log
import sys
import os
import json
import socket
import time
sys.path.append(os.path.join(os.getcwd(), '.'))


def create_message_to_server(acc_name="C0deMaver1ck"):
    message = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": acc_name,
        }
    }
    return message


def check_server_ans(answer):
    print(answer)
    if 'response' in answer:
        if answer['response'] == 200:
            return '200 : OK'
        return f"400 : {answer['error']}"
    raise ValueError


@log
def send_message():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = 'localhost'
        server_port = 7777
    except ValueError:
        print(
            'В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_address, server_port))
    create_message = create_message_to_server()
    s_m(server, create_message)
    try:
        msg = check_server_ans(get_message(server))
        print(msg)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    send_message()
