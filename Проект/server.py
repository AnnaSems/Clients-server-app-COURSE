""" Функции сервера: принимает сообщение клиента;
формирует ответ клиенту;
отправляет ответ клиенту;
имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса). """

import select
import sys
import socket
import sys
import argparse
import json
import time
from common.utils import get_message, send_message
from log.dec import log


def check_client_message(message, messages_list, client):
    if 'action' in message and message['action'] == 'authenticate' and 'time' in message \
            and 'user' in message and message['user']['account_name'] == 'C0deMaver1ck':
        send_message(client, {'response': 200})
        return
    elif 'action' in message and message['action'] == 'message' and 'time' in message \
            and 'mess_text' in message:
        messages_list.append((message['account_name'], message['mess_text']))
    send_message(client, {
        'code_error': 400,
        'error': 'Bad Request'
    })
    return


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=7777, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        print(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def create_answer():
    listen_address, listen_port = arg_parser()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_address, listen_port))
    server.settimeout(0.5)
    server.listen(4)

    clients = []
    messages = []

    while True:
        try:
            client, addr = server.accept()
        except OSError:
            pass
        else:
            print(f'Установлено соедение с ПК {listen_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(
                    clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    check_client_message(get_message(client_with_message),
                                         messages, client_with_message)
                except:
                    print(f'Клиент {client_with_message.getpeername()} '
                          f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                'action': 'message',
                'sender': messages[0][0],
                'time': time.time(),
                'mess_text': messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    print(
                        f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    create_answer()
