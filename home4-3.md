### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
   { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
import socket
import time
import json
import yaml

service_addr = {
    'drive.google.com': '0',
    'mail.google.com': '0',
    'google.com': '0'
}

for item in service_addr:
    initial_addr = socket.gethostbyname(item)
    service_addr[item] = initial_addr
    with open(item + '.json', 'w') as output_json:
        data_json = json.dumps({item: service_addr[item]})
        output_json.write(data_json)

    with open(item + '.yaml', 'w') as output_yaml:
        data_yaml = yaml.dump([{item: service_addr[item]}])
        output_yaml.write(data_yaml)

while True:
    for item in service_addr:
        old_addr = service_addr[item]
        new_addr = socket.gethostbyname(item)
        if new_addr != old_addr:
            service_addr[item] = new_addr
            with open(item + '.json', 'w') as output_json:
                data_json = json.dumps({item: service_addr[item]})
                output_json.write(data_json)

            with open(item + '.yaml', 'w') as output_yaml:
                data_yaml = yaml.dump([{item: service_addr[item]}])
                output_yaml.write(data_yaml)
            print("[ERROR] " + item + " IP mismatch: old IP " + old_addr + ", new IP " + new_addr)
        print(item + " - " + service_addr[item])
    print("######################################")
    time.sleep(10)
```

### Вывод скрипта при запуске при тестировании:
```
drive.google.com - 74.125.205.194
mail.google.com - 74.125.131.83
google.com - 142.251.1.102
######################################
drive.google.com - 74.125.205.194
[ERROR] mail.google.com IP mismatch: old IP 74.125.131.83, new IP 74.125.131.19
mail.google.com - 74.125.131.19
[ERROR] google.com IP mismatch: old IP 142.251.1.102, new IP 142.251.1.113
google.com - 142.251.1.113
######################################
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com": "74.125.205.194"}
{"google.com": "142.251.1.113"}
{"mail.google.com": "74.125.131.18"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com: 74.125.205.194
- google.com: 142.251.1.113
- mail.google.com: 74.125.131.18
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
???
```

### Пример работы скрипта:
???
