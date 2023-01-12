# Домашнее задание к занятию "8. MySQL"

------

## Задание 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
Изучите бэкап БД и восстановитесь из него.
Перейдите в управляющую консоль mysql внутри контейнера.
Используя команду \h получите список управляющих команд.
Найдите команду для выдачи статуса БД и приведите в ответе из ее вывода версию сервера БД.
Подключитесь к восстановленной БД и получите список таблиц из этой БД.
Приведите в ответе количество записей с price > 300.
В следующих заданиях мы будем продолжать работу с данным контейнером.

### Ответ:
```bash
version: '3.5'
services:
  mysql:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=test_db
    volumes:
      - ./data:/var/lib/mysql
      - ./backup:/data/backup/mysql
    ports:
      - "3306:3306"
    restart: always
```
```bash
vagrant@vagrant:~$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                                                  NAMES
bcaccd6d5390   mysql:8   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   mysql_mysql_1
```    
```bash
vagrant@vagrant:~$ sudo docker exec -it bcaccd6d5390 bash
bash-4.4# mysql -u root -p test_db < /data/backup/mysql/test_dump.sql
Enter password:
```
```bash
bash-4.4# mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 8.0.31 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
```bash
mysql> status
--------------
mysql  Ver 8.0.31 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:          12
Current database:
Current user:           root@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         8.0.31 MySQL Community Server - GPL
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    utf8mb4
Db     characterset:    utf8mb4
Client characterset:    latin1
Conn.  characterset:    latin1
UNIX socket:            /var/run/mysqld/mysqld.sock
Binary data as:         Hexadecimal
Uptime:                 23 min 13 sec
```
```bash
mysql> use test_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0.00 sec)
```
```bash
mysql> SELECT * FROM orders WHERE price > 300;
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0.01 sec)

mysql> SELECT count(*) FROM orders WHERE price > 300;
+----------+
| count(*) |
+----------+
|        1 |
+----------+
1 row in set (0.01 sec)
```
----

## Задание 2

В БД из задачи 1:
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

### Ответ:
```bash
CREATE USER "test-admin-user" WITH LOGIN;
CREATE DATABASE test_db;
CREATE TABLE orders (
	id SERIAL PRIMARY KEY, 
	наименование TEXT, 
	цена INT
);

CREATE TABLE clients (
	id SERIAL PRIMARY KEY, 
	фамилия TEXT, 
	"страна проживания" TEXT, 
	заказ INT REFERENCES orders (id)
);

CREATE INDEX ON clients ("страна проживания");

GRANT ALL ON TABLE clients, orders TO "test-admin-user";
CREATE USER "test-simple-user" WITH LOGIN;
GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE clients,orders TO "test-simple-user";
```
итоговый список БД после выполнения пунктов выше
```bash
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
(4 rows)
```
описание таблиц (describe)
```bash
                                                   Table "public.orders"
    Column    |  Type   | Collation | Nullable |              Default               | Storage  | Stats target | Description
--------------+---------+-----------+----------+------------------------------------+----------+--------------+-------------
 id           | integer |           | not null | nextval('orders_id_seq'::regclass) | plain    |              |
 наименование | text    |           |          |                                    | extended |              |
 цена         | integer |           |          |                                    | plain    |              |
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap
```
```bash
                                                      Table "public.clients"
      Column       |  Type   | Collation | Nullable |               Default               | Storage  | Stats target | Description
-------------------+---------+-----------+----------+-------------------------------------+----------+--------------+-------------
 id                | integer |           | not null | nextval('clients_id_seq'::regclass) | plain    |              |
 фамилия           | text    |           |          |                                     | extended |              |
 страна проживания | text    |           |          |                                     | extended |              |
 заказ             | integer |           |          |                                     | plain    |              |
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "clients_страна проживания_idx" btree ("страна проживания")
Foreign-key constraints:
    "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap
```
SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
```bash
SELECT table_name, array_agg(privilege_type), grantee
FROM information_schema.table_privileges
WHERE table_name = 'orders' OR table_name = 'clients'
GROUP BY table_name, grantee ;
```
список пользователей с правами над таблицами test_db
```bash
 table_name |                         array_agg                         |     grantee
------------+-----------------------------------------------------------+------------------
 clients    | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | postgres
 clients    | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | test-admin-user
 clients    | {DELETE,INSERT,SELECT,UPDATE}                             | test-simple-user
 orders     | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | postgres
 orders     | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | test-admin-user
 orders     | {DELETE,SELECT,UPDATE,INSERT}                             | test-simple-user
(6 rows)
```
---

## Задание 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders
| Наименование  | цена | 
| ------------- | ------------- |
| `Шоколад`  | 10  |
| `Принтер`  | 3000  |
| `Книга`  | 500  |
| `Монитор`  | 7000  |
| `Гитара`  | 4000  |

Таблица clients
| ФИО  | Страна проживания | 
| ------------- | ------------- |
| `Иванов Иван Иванович`  | USA  |
| `Петров Петр Петрович`  | Canada  |
| `Иоганн Себастьян Бах`  | Japan  |
| `Ронни Джеймс Дио`  | Russia  |
| `Ritchie Blackmore`  | Russia  |

Используя SQL синтаксис:

- вычислите количество записей для каждой таблицы
- приведите в ответе:
	- запросы
	- результаты их выполнения.

### Ответ:
```bash
INSERT INTO orders (наименование, цена )
VALUES 
    ('Шоколад', '10'),
    ('Принтер', '3000'),
    ('Книга', '500'),
    ('Монитор', '7000'),
    ('Гитара', '4000')
;
```
```bash
INSERT INTO clients ("фамилия", "страна проживания")
VALUES 
    ('Иванов Иван Иванович', 'USA'),
    ('Петров Петр Петрович', 'Canada'),
    ('Иоганн Себастьян Бах', 'Japan'),
    ('Ронни Джеймс Дио', 'Russia'),
    ('Ritchie Blackmore', 'Russia')
;
```
```bash
name_table | number_rows
------------+-------------
 orders     |           5
 clients    |           5
(2 rows)
```
```bash
SELECT 'orders' AS name_table,  COUNT(*) AS number_rows FROM orders
UNION ALL
SELECT 'clients' AS name_table,  COUNT(*) AS number_rows  FROM clients;
```

---
## Задание 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.
Используя foreign keys свяжите записи из таблиц, согласно таблице:

| ФИО  | Заказ | 
| ------------- | ------------- |
| `Иванов Иван Иванович`  | Книга  |
| `Петров Петр Петрович`  | Монитор  |
| `Иоганн Себастьян Бах`  | Гитара  |

Приведите SQL-запросы для выполнения данных операций.
Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.

### Ответ:
```bash
UPDATE clients SET "заказ"=18 WHERE id=16;
UPDATE clients SET "заказ"=19 WHERE id=17;
UPDATE clients SET "заказ"=20 WHERE id=18;

SELECT "фамилия","заказ",orders."наименование"
FROM clients
INNER JOIN orders ON "заказ"=orders."id";
```
```bash
       фамилия        | заказ | наименование
----------------------+-------+--------------
 Иванов Иван Иванович |    18 | Книга
 Петров Петр Петрович |    19 | Монитор
 Иоганн Себастьян Бах |    20 | Гитара
(3 rows)
```
