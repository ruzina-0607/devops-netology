## Домашнее задание к занятию 15 «Система сбора логов Elastic Stack»
---
## Задание 1
Вам необходимо поднять в докере и связать между собой:
- elasticsearch (hot и warm ноды);
- logstash;
- kibana;
- filebeat.
Logstash следует сконфигурировать для приёма по tcp json-сообщений.

Filebeat следует сконфигурировать для отправки логов docker вашей системы в logstash.

В директории help находится манифест docker-compose и конфигурации filebeat/logstash для быстрого выполнения этого задания.

Результатом выполнения задания должны быть:
- скриншот docker ps через 5 минут после старта всех контейнеров (их должно быть 5);
- скриншот интерфейса kibana;
- docker-compose манифест (если вы не использовали директорию help);
- ваши yml-конфигурации для стека (если вы не использовали директорию help).

![image](https://github.com/ruzina-0607/devops-netology/assets/104915472/9ad96b67-e9b6-42f5-91e6-fe0aaec25c09)
![image](https://github.com/ruzina-0607/devops-netology/assets/104915472/21cd810d-e117-4986-9d5f-d5f0a436d0fa)


## Задание 2
Перейдите в меню создания index-patterns в kibana и создайте несколько index-patterns из имеющихся.

Перейдите в меню просмотра логов в kibana (Discover) и самостоятельно изучите, как отображаются логи и как производить поиск по логам.

В манифесте директории help также приведенно dummy-приложение, которое генерирует рандомные события в stdout-контейнера. Эти логи должны порождать индекс logstash-* в elasticsearch. Если этого индекса нет — воспользуйтесь советами и источниками из раздела «Дополнительные ссылки» этого задания.
![image](https://github.com/ruzina-0607/devops-netology/assets/104915472/ed2dba09-6a53-4736-bc6c-bf7e0461ed98)
![image](https://github.com/ruzina-0607/devops-netology/assets/104915472/fafd4e72-1d71-42ad-8fa4-bbf1c1436892)

