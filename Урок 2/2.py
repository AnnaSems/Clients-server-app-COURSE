""" 2. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
количество (quantity), цена (price), покупатель (buyer), дата (date). 
Функция должна предусматривать запись данных в виде словаря в файл orders.json. 
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра. """


import json


def write_order_to_json(items, quantity, price, buyer, date):
    data = {'items':items, 'quantity': quantity, 'price':price,
            'buyer': buyer, 'date': date}
    with open("orders.json", encoding='UTF-8') as w_file:
        json_file = json.load(w_file)
        json_file['orders'].append(data)

    with open("orders.json", 'w', encoding='UTF-8') as write_file:
        json.dump(json_file, write_file, indent=4)

write_order_to_json(5, 5, 5, '545', '12.11.2011')
write_order_to_json(5, 5, 5, '54f', '12.11.2011')