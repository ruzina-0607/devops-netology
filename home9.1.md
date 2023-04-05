Домашнее задание к занятию 9.1 «Жизненный цикл ПО»

------
## Задание 1
## Основная часть
Необходимо создать собственные workflow для двух типов задач: bug и остальные типы задач. Задачи типа bug должны проходить жизненный цикл:
Open -> On reproduce.
On reproduce -> Open, Done reproduce.
Done reproduce -> On fix.
On fix -> On reproduce, Done fix.
Done fix -> On test.
On test -> On fix, Done.
Done -> Closed, Open.

<img width="692" alt="image" src="https://user-images.githubusercontent.com/104915472/230199191-50c995db-8293-4a2c-9450-c9e477a9835f.png">


Остальные задачи должны проходить по упрощённому workflow:
Open -> On develop.
On develop -> Open, Done develop.
Done develop -> On test.
On test -> On develop, Done.
Done -> Closed, Open.

<img width="391" alt="image" src="https://user-images.githubusercontent.com/104915472/230201826-68c37084-e5b6-48c3-b590-898292b738b2.png">


Что нужно сделать
Создайте задачу с типом bug, попытайтесь провести его по всему workflow до Done.
Создайте задачу с типом epic, к ней привяжите несколько задач с типом task, проведите их по всему workflow до Done.
При проведении обеих задач по статусам используйте kanban.
Верните задачи в статус Open.
Перейдите в Scrum, запланируйте новый спринт, состоящий из задач эпика и одного бага, стартуйте спринт, проведите задачи до состояния Closed. Закройте спринт.
Если всё отработалось в рамках ожидания — выгрузите схемы workflow для импорта в XML. Файлы с workflow приложите к решению задания.
