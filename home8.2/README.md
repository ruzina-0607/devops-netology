Плейбук предназначен для установки Clickhouse и Vector на хосты, которые указаны в inventory.

## group_vars
| Переменная  | Значение |
| ------------- | ------------- |
| clickhouse_version  | версия Clickhouse  |
| vector_url  | URL адрес для скачивания RPM пакетов Vector  |
| clickhouse_packages  | RPM пакеты Clickhouse, которые необходимо скачать  |
| vector_versionl  | версия Vector  |
| vector_home  | каталог для скачивания RPM пакетов Vector |

## Inventory файл
Группа clickhouse состоит из 1 хоста clickhouse-01 
Группа vector состоит из 1 хоста vector-01

## Playbook 
Playbook состоит из 3 play.
Play Install Clickhouse применяется на группу хостов Clickhouse и предназначен для установки и запуска Clickhouse

handler предназначен для запуска clickhouse-server.
```bash
handlers:
    - name: Start clickhouse service
      become: true
      ansible.builtin.service:
        name: clickhouse-server
        state: restarted
```
| Наименование таски  | Описание |
| ------------- | ------------- |
| Clickhouse\Get clickhouse distrib  | Скачивание RPM пакетов. Используется цикл с перменными clickhouse_packages. Так как не у всех пакетов есть noarch версии, используем перехват ошибки rescue  |
| Clickhouse\Install clickhouse packages  | Установка RPM пакетов. Исп. disable_gpg_check: true для отключения проверки GPG подписи пакетов. В notify указ., что  таск требует запуск handler Start clickhouse service  |
| Clickhouse\Flush handlers  | Применение handler Start clickhouse service. handler должен выполниться на текущем этапе, а не по завершению тасок. Если его не запустить сейчас, то сервис не будет запущен и следующий таск завершится с ошибкой  |
| Clickhouse\Create database  | Создание в Clickhouse БД с названием "logs". И прописываем условия, при которых таск будет иметь состояние failed и changed  |


Play Install Vector применяется на группу хостов Vector и предназначен для установки и запуска Vector. Задание handler для запуска vector.
```bash
 handlers:
    - name: Start Vector service
      become: true
      ansible.builtin.service:
        name: vector
        state: restarted
```
| Наименование таски  | Описание |
| ------------- | ------------- |
| Vector\Download packages  | Скачивание RPM пакетов в текущую директорию пользователя  |
| Vector\Install packages  | Установка RPM пакетов. Исп. disable_gpg_check: true для отключения проверки GPG подписи пакетов  |
| Vector\Apply template  | Применение шаблона конфига vector: задание пути конфига, а владельцем назначен текущий пользователя ansible. После применения запускается валидация конфига  |
| Vector\change systemd unit  | Изменяется модуль службы vector. После этого указывается handler для старта службы vector  |


## Template 
Шаблон "vector.service.j2" используется для изменения модуля службы vector. В нем определятеся строка запуска vector, unit должен запущен под текущим пользователем ansible.

Шаблон "vector.yml.j2" используется для настройки конфига vector. В нем указывается, что конфиг файл находится в переменной "vector_config" и его надо преобразовать в YAML.
