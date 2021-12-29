""" 3. Подготовить данные для записи в виде словаря, 
в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. 
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, 
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными. """

import yaml
import re

def write_to_yaml(lst:list, num:int, dictionary:dict):
    data = {

    }
    if type(lst) == list:
      data['list'] = lst

    if type(num) == int:
      data['integer'] = num

    if type(dictionary) == dict:
      for key in dictionary.keys():
        match = re.match(r'[0-9]', key)
        match_dot = re.findall(r'[.]', key)
        if (not key.isascii()) and match and (not match_dot):
            data['dictionary'] = dictionary

    with open('file.yaml', 'w', encoding='UTF-8') as f:
        yaml.dump(data, f, default_flow_style=True, allow_unicode = True)

    with open('file.yaml') as f_n:
        print(f_n.read())

write_to_yaml([2,3], 12, {"12€": '12'})