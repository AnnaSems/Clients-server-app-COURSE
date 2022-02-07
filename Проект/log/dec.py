import sys
import logging
from time import strftime
import traceback


if sys.argv[0].find('client.py') == 0:
    LOG = logging.getLogger('client')
else:
    LOG = logging.getLogger('server')


def log(func):
    def decorated(*args, **kwargs):
        main = func(*args, **kwargs)
        call_time = strftime("%a, %d %b %Y %H:%M:%S")
        LOG.debug(
            f'Функция {func.__name__} с параметрами {args} {kwargs} была вызвана в {call_time}'
            f'из модуля {func.__module__}'
            f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}')
        return main
    return decorated
