from ipaddress import ip_address
from subprocess import Popen
from telnetlib import IP
from tkinter import N
from tabulate import tabulate

# Проверяет доступность сетевых узлов


def is_ip_address(address):
    try:
        ip_address(address)
    except ValueError:
        return f'{address} does not appear to be an IPv4 or IPv6 address'
    return str(ip_address(address))


def host_ping(main_address, lst):
    host_result_reachable = []
    host_result_unreachable = []
    for i in range(len(lst)):
        args = ['ping', '-c', '1', f'{main_address}/{str(lst[i])}']
        reply = Popen(args)
        code = reply.wait()
        if code == 0:
            host_result_reachable.append(
                f'{main_address}/{str(lst[i])}')
        else:
            host_result_unreachable.append(
                f'{main_address}/{str(lst[i])}')
    return [host_result_reachable, host_result_unreachable]


# Перебор одресов из заданного диапозон
def host_range_ping(address, num: int):
    main_address = is_ip_address(address)
    try:
        last_oct = int(main_address.split('.')[3])
    except ValueError:
        return f'{main_address} does not appear to be an IPv4 or IPv6 address'
    if (last_oct + num) > 255:
        return 'The last octet cannot be greater than 255'
    host_address = []
    [host_address.append(str(last_oct+x)) for x in range(num)]
    return host_ping(main_address, host_address)


result_list = host_range_ping('127.0.0.1', 8)


def host_range_ping_tab(result_list):
    vlan = [{'reachable': result_list[0]}, {'unreachable': result_list[1]}]
    return tabulate(vlan, headers='keys')
