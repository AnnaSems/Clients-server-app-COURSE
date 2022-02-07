""" Функции клиента: сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777. """

import sys
import os
import json
import socket
import time
import argparse
import threading
from common.utils import get_message, send_message as s_m
from log.dec import log
sys.path.append(os.path.join(os.getcwd(), '.'))


def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if 'action' in message and message['action'] == 'message' and \
                    'from' in message and 'mess_text' in message and message['to'] == my_username:
                print(f'Получено сообщение от пользователя '
                      f'{message["from"]}:\n{message["mess_text"]}')
                print(f'Получено сообщение от пользователя '
                      f'{message["from"]}:\n{message["mess_text"]}')
            else:
                print(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            print(f'Потеряно соединение с сервером.')
            break


@log
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        'action': 'exit',
        'time': time.time(),
        'account_name': account_name
    }


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


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            s_m(sock, create_exit_message(username))
            print('Завершение соединения.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print(
                'Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


def create_message_to_server(acc_name="C0deMaver1ck"):
    message = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": acc_name,
        }
    }
    return message


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


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
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
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
    server_address, server_port, client_name = arg_parser()

    # Инициализация сокета и сообщение серверу о нашем появлении
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        s_m(transport, create_message_to_server())
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        receiver = threading.Thread(
            target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(
            target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
