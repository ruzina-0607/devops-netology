#!/usr/bin/env python3

import socket
import time
import json
import yaml

# задаем словарь
service_addr = {
    'drive.google.com': '0',
    'mail.google.com': '0',
    'google.com': '0'
}

# Получаем текущие на момент запуска скрипта значения (чтобы в будущем не сравнивать с 0).
for item in service_addr:
    initial_addr = socket.gethostbyname(item)
    service_addr[item] = initial_addr
    # Записываем полученные данные в виде json файла
    with open(item + '.json', 'w') as output_json:
        # Формируем json
        data_json = json.dumps({item: service_addr[item]})
        # Записываем его в файл
        output_json.write(data_json)

    # Записываем полученные данные в виде yaml файла
    with open(item + '.yaml', 'w') as output_yaml:
        # Формируем yaml
        data_yaml = yaml.dump([{item: service_addr[item]}])
        # Записываем его в файл
        output_yaml.write(data_yaml)

while True:
    # Перебираем все ключи в словаре
    for item in service_addr:
        old_addr = service_addr[item]
        new_addr = socket.gethostbyname(item)
        # Если старое и новое не совпадают - адрес изменился. Перезаписываем значение в словаре и выводим ошибку
        if new_addr != old_addr:
            service_addr[item] = new_addr
            # Записываем полученные данные в виде json файла
            with open(item + '.json', 'w') as output_json:
                # Формируем json
                data_json = json.dumps({item: service_addr[item]})
                # Записываем его в файл
                output_json.write(data_json)

            # Записываем полученные данные в виде yaml файла
            with open(item + '.yaml', 'w') as output_yaml:
                # Формируем yaml
                data_yaml = yaml.dump([{item: service_addr[item]}])
                # Записываем его в файл
                output_yaml.write(data_yaml)
            # Вывод ошибки
            print("[ERROR] " + item + " IP mismatch: old IP " + old_addr + ", new IP " + new_addr)
        print(item + " - " + service_addr[item])
    print("######################################")
    time.sleep(10)
