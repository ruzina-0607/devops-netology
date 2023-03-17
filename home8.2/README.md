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
Группа "clickhouse" состоит из 1 хоста clickhouse-01 Группа "vector" состоит из 1 хоста vector-01

###Playbook Playbook состоит из 3 play.

Play "Install Clickhouse" применяется на группу хостов "Clickhouse" и предназначен для установки и запуска Clickhouse

Объявляем handler для запуска clickhouse-server.

handlers:
    - name: Start clickhouse service
      become: true
      ansible.builtin.service:
        name: clickhouse-server
        state: restarted
Переменная	Значение
Get clickhouse distrib	Скачивание RPM пакетов. Используется цикл с перменными clickhouse_packages. Так как не у всех пакетов есть noarch версии, используем перехват ошибки rescue
Clickhouse	Install clickhouse packages
Clickhouse	Flush handlers
Clickhouse	Create database
Play "Install Vector" применяется на группу хостов "Vector" и предназначен для установки и запуска Vector

Объявляем handler для запуска vector.

 handlers:
    - name: Start Vector service
      become: true
      ansible.builtin.service:
        name: vector
        state: restarted
Переменная	Значение
Vector	Download packages
Vector	Install packages
Vector	Apply template
Vector	change systemd unit
###Template Шаблон "vector.service.j2" используется для изменения модуля службы vector. В нем мы определяем строку запуска vector. Также указываем, что unit должен быть запущен под текущим пользователем ansible

Шаблон "vector.yml.j2" используется для настройки конфига vector. В нем мы указываем, что конфиг файл находится в переменной "vector_config" и его надо преобразовать в YAML.
