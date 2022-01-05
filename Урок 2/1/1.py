""" 1. Задание на закрепление знаний по модулю CSV. 
Написать скрипт, осуществляющий выборку определенных данных из файлов 
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. """

import csv
import re

FILES_LST = ['info_1.txt', 'info_2.txt', 'info_2.txt']


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []
    for i in FILES_LST:
        with open(i, encoding='cp1251') as f_r:
            for el in f_r:
                el = el.encode(encoding='UTF-8').decode(encoding='UTF-8')
                find_string_prod = re.search(r'Изготовитель системы', el)
                find_string_name = re.search(r'Название ОС', el)
                find_string_code = re.search(r'Код продукта', el)
                find_string_type = re.search(r'Тип системы', el)
                if find_string_prod != None:
                    os_prod_list.append(el.partition(
                        '  ')[2].lstrip().rstrip())
                if find_string_name != None:
                    os_name_list.append(el.partition(
                        '  ')[2].lstrip().rstrip())
                if find_string_code != None:
                    os_code_list.append(el.partition(
                        '  ')[2].lstrip().rstrip())
                if find_string_type != None:
                    os_type_list.append(el.partition(
                        '  ')[2].lstrip().rstrip())
    headers = ['Изготовитель системы',
               'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)
    data = [os_prod_list, os_name_list, os_code_list, os_type_list]
    for el in range(len(data[0])):
        row = [el_data[el] for el_data in data]
        main_data.append(row)

    return main_data


def write_to_csv(file):
    data = get_data()
    with open(file, 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        f_n_writer.writerows(data)

    with open(file) as f_n:
        print(f_n.read())


write_to_csv('report.csv')
