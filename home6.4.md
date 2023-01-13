Домашнее задание к занятию "9. PostgreSQL"

------

## Задание 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
Подключитесь к БД PostgreSQL используя psql.
Воспользуйтесь командой \? для вывода подсказки по имеющимся в psql управляющим командам.
Найдите и приведите управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ:
```bash
version: '3.5'
services:
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
    volumes:
      - ./data:/var/lib/postgresql/data
      - ./backup:/data/backup/postgres
    ports:
      - "5432:5432"
    restart: always
```
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
(3 rows)
```    
```bash
postgres=# \c postgres
You are now connected to database "postgres" as user "postgres".
```
```bash
postgres=# \dt
Did not find any relations.
postgres=# \dt+
Did not find any relations.
```
```bash
postgres=# \d pg_database
               Table "pg_catalog.pg_database"
    Column     |   Type    | Collation | Nullable | Default
---------------+-----------+-----------+----------+---------
 oid           | oid       |           | not null |
 datname       | name      |           | not null |
 datdba        | oid       |           | not null |
 encoding      | integer   |           | not null |
 datcollate    | name      |           | not null |
 datctype      | name      |           | not null |
 datistemplate | boolean   |           | not null |
 datallowconn  | boolean   |           | not null |
 datconnlimit  | integer   |           | not null |
 datlastsysoid | oid       |           | not null |
 datfrozenxid  | xid       |           | not null |
 datminmxid    | xid       |           | not null |
 dattablespace | oid       |           | not null |
 datacl        | aclitem[] |           |          |
Indexes:
    "pg_database_datname_index" UNIQUE, btree (datname), tablespace "pg_global"
    "pg_database_oid_index" UNIQUE, btree (oid), tablespace "pg_global"
Tablespace: "pg_global"
```
```bash
postgres=# \q
```
----

## Задание 2

Используя psql создайте БД test_database.
Изучите бэкап БД.
Восстановите бэкап БД в test_database.
Перейдите в управляющую консоль psql внутри контейнера.
Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
Используя таблицу pg_stats, найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах.
Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.

### Ответ:
```bash
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
```
```bash
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
```
```bash
postgres@vagrant:~$ psql -U postgres test_database < test_dump.sql
SET
SET
SET
SET
SET
 set_config
------------

(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval
--------
      8
(1 row)

ALTER TABLE
```
```bash
postgres=# \l
                                    List of databases
     Name      |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
---------------+----------+----------+-------------+-------------+-----------------------
 postgres      | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0     | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
               |          |          |             |             | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
               |          |          |             |             | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
(4 rows)
```
```bash
postgres=# \c test_database
You are now connected to database "test_database" as user "postgres".
test_database=# \d
              List of relations
 Schema |     Name      |   Type   |  Owner
--------+---------------+----------+----------
 public | orders        | table    | postgres
 public | orders_id_seq | sequence | postgres
(2 rows)

test_database=# analyze verbose public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```
```bash
test_database=# SELECT tablename, attname, avg_width FROM pg_stats WHERE avg_width IN (SELECT MAX(avg_width) FROM pg_stats WHERE tablename = 'orders') and tablename = 'orders';
 tablename | attname | avg_width
-----------+---------+-----------
 orders    | title   |        16
(1 row)
```
---

## Задание 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
Предложите SQL-транзакцию для проведения данной операции.

### Ответ:
```bash
test_database=# BEGIN;
BEGIN
test_database=# ALTER TABLE orders RENAME TO orders_old;
ALTER TABLE
test_database=# CREATE TABLE orders AS table orders_old WITH NO DATA;
CREATE TABLE AS
test_database=# CREATE TABLE orders_1 (
test_database(#     CHECK (price > 499)
test_database(# ) INHERITS (orders);
CREATE TABLE
test_database=# CREATE TABLE orders_2 (
test_database(#     CHECK (price <= 499)
test_database(# ) INHERITS (orders);
CREATE TABLE
test_database=# CREATE RULE orders_1_insert AS
test_database-# ON INSERT TO orders WHERE
test_database-#     (price > 499)
test_database-# DO INSTEAD
test_database-#     INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE
test_database=# CREATE RULE orders_2_insert AS
test_database-# ON INSERT TO orders WHERE
test_database-#     (price <= 499)
test_database-# DO INSTEAD
test_database-#     INSERT INTO orders_2 VALUES (NEW.*);
CREATE RULE
test_database=# INSERT INTO orders
test_database-# SELECT * FROM orders_old;
INSERT 0 0
test_database=# COMMIT;
COMMIT
test_database=# \d
              List of relations
 Schema |     Name      |   Type   |  Owner
--------+---------------+----------+----------
 public | orders        | table    | postgres
 public | orders_1      | table    | postgres
 public | orders_2      | table    | postgres
 public | orders_id_seq | sequence | postgres
 public | orders_old    | table    | postgres
(5 rows)

test_database=# TABLE orders_1;
 id |       title        | price
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)

test_database=# TABLE orders_2;
 id |        title         | price
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)

test_database=# TABLE orders;
 id |        title         | price
----+----------------------+-------
  2 | My little database   |   500
  6 | WAL never lies       |   900
  8 | Dbiezdmin            |   501
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(8 rows)
```
Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?
```bash
test_database=# CREATE TABLE orders (
test_database(#     id integer NOT NULL,
test_database(#     title character varying(80) NOT NULL,
test_database(#     price integer DEFAULT 0
test_database(# ) PARTITION BY RANGE (price);
```
Создание секции orders_1 и orders_2 с указанными ограничениями
```bash
test_database=# CREATE TABLE orders_1 PARTITION OF orders
test_database-#     FOR VALUES GREATER THAN ('499');
```
```bash
test_database=# CREATE TABLE orders_2 PARTITION OF orders
test_database-#     FOR VALUES FROM ('0') TO ('499');
```
Старая таблица теперь называется orders_old. Новая таблица - orders. Создала 2 таблицы с наследованием от orders. Создала ограничение на ключ price.
Создала правила, , при которых INSERT в таблицу orders будет заменяться на INSERT в дочернюю таблицу (в зависимости от значения ключа price)
Далее происходит копирование через INSERT таблицу orders_old в orders SQL транзакция.
---
## Задание 4

Используя утилиту pg_dump создайте бекап БД test_database.
Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца title для таблиц test_database?

### Ответ:
```bash
postgres@vagrant:~$ pg_dump -U postgres -v -f test_database.sql
pg_dump: last built-in OID is 16383
pg_dump: reading extensions
pg_dump: identifying extension members
pg_dump: reading schemas
pg_dump: reading user-defined tables
pg_dump: reading user-defined functions
pg_dump: reading user-defined types
pg_dump: reading procedural languages
pg_dump: reading user-defined aggregate functions
pg_dump: reading user-defined operators
pg_dump: reading user-defined access methods
pg_dump: reading user-defined operator classes
pg_dump: reading user-defined operator families
pg_dump: reading user-defined text search parsers
pg_dump: reading user-defined text search templates
pg_dump: reading user-defined text search dictionaries
pg_dump: reading user-defined text search configurations
pg_dump: reading user-defined foreign-data wrappers
pg_dump: reading user-defined foreign servers
pg_dump: reading default privileges
pg_dump: reading user-defined collations
pg_dump: reading user-defined conversions
pg_dump: reading type casts
pg_dump: reading transforms
pg_dump: reading table inheritance information
pg_dump: reading event triggers
pg_dump: finding extension tables
pg_dump: finding inheritance relationships
pg_dump: reading column info for interesting tables
pg_dump: flagging inherited columns in subtables
pg_dump: reading indexes
pg_dump: flagging indexes in partitioned tables
pg_dump: reading extended statistics
pg_dump: reading constraints
pg_dump: reading triggers
pg_dump: reading rewrite rules
pg_dump: reading policies
pg_dump: reading row-level security policies
pg_dump: reading publications
pg_dump: reading publication membership
pg_dump: reading subscriptions
pg_dump: reading large objects
pg_dump: reading dependency data
pg_dump: saving encoding = UTF8
pg_dump: saving standard_conforming_strings = on
pg_dump: saving search_path =
pg_dump: implied data-only restore
```
```bash
test_database=# CREATE TABLE public.orders (
test_database(#     id integer NOT NULL,
test_database(#     title character varying(80) NOT NULL UNIQUE,
test_database(#     price integer DEFAULT 0
test_database(# );
```
