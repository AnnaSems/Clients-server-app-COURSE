""" Функции клиента: сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777. """

import argparse
from common.utils import get_message, send_message as s_m
from log.dec import log
import sys
import os
import json
import socket
import time
sys.path.append(os.path.join(os.getcwd(), '.'))


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if 'action' in message and message['action'] == 'message' and \
            'sender' in message and 'mess_text' in message:
        print(f'Получено сообщение от пользователя '
              f'{message["sender"]}:\n{message["mess_text"]}')
        print(f'Получено сообщение от пользователя '
              f'{message["sender"]}:\n{message["mess_text"]}')
    else:
        print(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input(
        'Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        print('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        'action': 'message',
        'time': time.time(),
        'account_name': account_name,
        'mess_text': message
    }
    print(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


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
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default='localhost', nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        print(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        print(f'Указан недопустимый режим работы {client_mode}, '
              f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    """Загружаем параметы коммандной строки"""
    server_address, server_port, client_mode = arg_parser()

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        s_m(transport, create_message_to_server())
        answer = check_server_ans(get_message(transport))
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    s_m(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    sys.exit(1)


if __name__ == '__main__':
    main()
