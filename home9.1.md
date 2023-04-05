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
<img width="594" alt="image" src="https://user-images.githubusercontent.com/104915472/230207913-9e6c487c-3126-49d8-9ebe-b6b9a23cd04a.png">
<img width="786" alt="image" src="https://user-images.githubusercontent.com/104915472/230209743-5141a957-3e15-49e4-97a8-f2ccf0f8e5ad.png">


## Что нужно сделать
Создайте задачу с типом bug, попытайтесь провести его по всему workflow до Done.
Создайте задачу с типом epic, к ней привяжите несколько задач с типом task, проведите их по всему workflow до Done.
<img width="717" alt="image" src="https://user-images.githubusercontent.com/104915472/230207263-abaeaeeb-dc11-4bde-b1f9-50c841bc17d2.png">

При проведении обеих задач по статусам используйте kanban.
Верните задачи в статус Open.
<img width="798" alt="image" src="https://user-images.githubusercontent.com/104915472/230207166-b0d1fb7b-7ee8-48d7-bc1c-da15b5bcdba8.png">

Перейдите в Scrum, запланируйте новый спринт, состоящий из задач эпика и одного бага, стартуйте спринт, проведите задачи до состояния Closed. Закройте спринт.
Если всё отработалось в рамках ожидания — выгрузите схемы workflow для импорта в XML. Файлы с workflow приложите к решению задания. 
<img width="545" alt="image" src="https://user-images.githubusercontent.com/104915472/230208690-18fc5663-0109-4fd1-984a-b563cae50c16.png">
<img width="803" alt="image" src="https://user-images.githubusercontent.com/104915472/230209315-ac12df07-15de-41e1-9d63-5f5506e44cc0.png">

