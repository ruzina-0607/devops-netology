### Домашнее задание к занятию 4 «Работа с roles»

## Основная часть
Ваша цель — разбить ваш playbook на отдельные roles.
Задача — сделать roles для ClickHouse, Vector и LightHouse и написать playbook для использования этих ролей.
Ожидаемый результат — существуют три ваших репозитория: два с roles и один с playbook.

## Что нужно сделать
1. Создайте в старой версии playbook файл requirements.yml и заполните его содержимым:
```bash
---
  - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
    scm: git
    version: "1.11.0"
    name: clickhouse 
```
2. При помощи ansible-galaxy скачайте себе эту роль.
3. Создайте новый каталог с ролью при помощи ansible-galaxy role init vector-role.
4. На основе tasks из старого playbook заполните новую role. Разнесите переменные между vars и default.
5. Перенести нужные шаблоны конфигов в templates.
6. Опишите в README.md обе роли и их параметры.
7. Повторите шаги 3–6 для LightHouse. Помните, что одна роль должна настраивать один продукт.
8. Выложите все roles в репозитории. Проставьте теги, используя семантическую нумерацию. Добавьте roles в requirements.yml в playbook.
https://github.com/ruzina-0607/vector-role/blob/1.0.0/home8.4.md
https://github.com/ruzina-0607/lighthouse-role/blob/1.0.0/home8.4.md
9. Переработайте playbook на использование roles. Не забудьте про зависимости LightHouse и возможности совмещения roles с tasks.
10. Выложите playbook в репозиторий.
11. В ответе дайте ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.
https://github.com/ruzina-0607/vector-role/tree/1.0.0
https://github.com/ruzina-0607/lighthouse-role
https://github.com/ruzina-0607/devops-netology/tree/main/home8.4
