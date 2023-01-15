Домашнее задание к занятию "10. Elasticsearch"

------

## Задание 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ centos:7 как базовый и документацию по установке и запуску Elastcisearch:
- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте push в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути / c хост-машины

Требования к elasticsearch.yml:
- данные path должны сохраняться в /var/lib
- имя ноды должно быть netology_test

### Ответ:
Dockerfile
```bash
FROM centos:centos7

RUN yum -y install wget; yum clean all && \
        groupadd --gid 1000 elasticsearch && \
        adduser --uid 1000 --gid 1000 --home /usr/share/elasticsearch elasticsearch && \
        mkdir /var/lib/elasticsearch/ && \
        chown -R elasticsearch:elasticsearch /var/lib/elasticsearch/ && \
        mkdir /var/log/elasticsearch/ && \
        chown -R elasticsearch:elasticsearch /var/log/elasticsearch/

USER elasticsearch

WORKDIR /usr/share/elasticsearch

ENV EL_VER=8.6.0

RUN wget https://fossies.org/linux/www/elasticsearch-${EL_VER}-linux-x86_64.tar.gz && \
        tar -xzf elasticsearch-${EL_VER}-linux-x86_64.tar.gz && \
        cp -rp elasticsearch-${EL_VER}/* ./ && \
        rm -rf elasticsearch-${EL_VER}*

COPY elasticsearch.yml /usr/share/elasticsearch/config/

EXPOSE 9200

CMD ["bin/elasticsearch"]
```
Elasticsearch.yml
```bash
# ======================== Elasticsearch Configuration =========================
#
# NOTE: Elasticsearch comes with reasonable defaults for most settings.
#       Before you set out to tweak and tune the configuration, make sure you
#       understand what are you trying to accomplish and the consequences.
#
# The primary way of configuring a node is via this file. This template lists
# the most important settings you may want to configure for a production cluster.
#
# Please consult the documentation for further information on configuration options:
# https://www.elastic.co/guide/en/elasticsearch/reference/index.html
#
# ---------------------------------- Cluster -----------------------------------
#
# Use a descriptive name for your cluster:
#
cluster.name: my-cluster
#
# ------------------------------------ Node ------------------------------------
#
# Use a descriptive name for the node:
#
node.name: netology_test
#
# Add custom attributes to the node:
#
#node.attr.rack: r1
#
# ----------------------------------- Paths ------------------------------------
#
# Path to directory where to store the data (separate multiple locations by comma):
#
path.data: /var/lib/elasticsearch
#
# Path to log files:
#
path.logs: /var/log/elasticsearch
#
# ----------------------------------- Memory -----------------------------------
#
# Lock the memory on startup:
#
#bootstrap.memory_lock: true
#
# Make sure that the heap size is set to about half the memory available
# on the system and that the owner of the process is allowed to use this
# limit.
#
# Elasticsearch performs poorly when the system is swapping the memory.
#
# ---------------------------------- Network -----------------------------------
#
# Set the bind address to a specific IP (IPv4 or IPv6):
#
#network.host: 192.168.0.1
network.host: 0.0.0.0
#
# Set a custom port for HTTP:
#
http.port: 9200
#
# For more information, consult the network module documentation.
#
# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
#discovery.seed_hosts: [127.0.0.1]
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
#cluster.initial_master_nodes: ["netology_test"]
#
# For more information, consult the discovery and cluster formation module documentation.
#
# ---------------------------------- Gateway -----------------------------------
#
# Block initial recovery after a full cluster restart until N nodes are started:
#
#gateway.recover_after_nodes: 3
#
# For more information, consult the gateway module documentation.
#
# ---------------------------------- Various -----------------------------------
#
# Require explicit names when deleting indices:
#
#action.destructive_requires_name: true
xpack.security.enabled: false
discovery.type: single-node
path.repo: /usr/share/elasticsearch/snapshots
```    
ответ elasticsearch на запрос пути / в json виде
```bash
vagrant@vagrant:~$ curl -u elastic:elastic http://localhost:9200
{
  "name" : "netology_test",
  "cluster_name" : "my-cluster",
  "cluster_uuid" : "5PBNFyzXSwuhc_X9BI4A_g",
  "version" : {
    "number" : "8.6.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "f67ef2df40237445caa70e2fef79471cc608d70d",
    "build_date" : "2023-01-04T09:35:21.782467981Z",
    "build_snapshot" : false,
    "lucene_version" : "9.4.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


----

## Задание 2

Ознакомтесь с документацией и добавьте в elasticsearch 3 индекса, в соответствии со таблицей.
Получите список индексов и их статусов, используя API и приведите в ответе на задание.
Получите состояние кластера elasticsearch, используя API.
Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
Удалите все индексы.

### Ответ:
```bash
vagrant@vagrant:~$ curl -u elastic:changeme -X PUT http://localhost:9200/ind-1?pretty -H 'Content-Type: application/json' -d'{ "settings": { "index": { "number_of_shards": 1, "number_of_replicas": 0 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
vagrant@vagrant:~$ curl -u elastic:changeme -X PUT http://localhost:9200/ind-2?p
retty -H 'Content-Type: application/json' -d'{ "settings": { "index": { "number_
of_shards": 2, "number_of_replicas": 1 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
vagrant@vagrant:~$ curl -u elastic:changeme -X PUT http://localhost:9200/ind-3?p
retty -H 'Content-Type: application/json' -d'{ "settings": { "index": { "number_
of_shards": 4, "number_of_replicas": 2 }}}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
```
```bash
vagrant@vagrant:~$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   ind-1 3UfinhDHTeyi2VsJddNHcw   1   0          0            0       225b           225b
yellow open   ind-3 gE2GLTMCQbi3-BAJJrYTLw   4   2          0            0       900b           900b
yellow open   ind-2 eTtBKJB2SsyNseuVnrxeYw   2   1          0            0       450b           450b
```
```bash
vagrant@vagrant:~$ curl -X GET 'http://localhost:9200/_cluster/health?pretty'
{
  "cluster_name" : "my-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 8,
  "active_shards" : 8,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 44.44444444444444
}
```
Возможно индексы и кластер находятся в yellow, потому что при создании индексов указывала количество реплик больше 1. 
В кластере 1 нода, поэтому реплицировать индексы некуда.



---

## Задание 3

Установите профилирование SET profiling = 1. Изучите вывод профилирования команд SHOW PROFILES;.
Исследуйте, какой engine используется в таблице БД test_db и приведите в ответе.
Измените engine и приведите время выполнения и запрос на изменения из профайлера в ответе:
- на MyISAM
- на InnoDB

### Ответ:
```bash
mysql> use test_db
Database changed
mysql> SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> show profiles;
+----------+------------+-------------------+
| Query_ID | Duration   | Query             |
+----------+------------+-------------------+
|        1 | 0.00079250 | SELECT DATABASE() |
|        2 | 0.00212975 | SET profiling = 1 |
+----------+------------+-------------------+
2 rows in set, 1 warning (0.00 sec)

mysql> SELECT TABLE_NAME,
    ->         ENGINE
    -> FROM   information_schema.TABLES
    -> WHERE  TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.00 sec)

mysql> alter table orders engine = myisam;
Query OK, 5 rows affected (0.09 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> alter table orders engine = innodb;
Query OK, 5 rows affected (0.13 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> show profiles;
+----------+------------+----------------------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                              |
+----------+------------+----------------------------------------------------------------------------------------------------+
|        1 | 0.00079250 | SELECT DATABASE()                                                                                  |
|        2 | 0.00212975 | SET profiling = 1                                                                                  |
|        3 | 0.01110450 | SELECT TABLE_NAME,
        ENGINE
FROM   information_schema.TABLES
WHERE  TABLE_SCHEMA = 'test_db' |
|        4 | 0.09306300 | alter table orders engine = myisam                                                                 |
|        5 | 0.12104525 | alter table orders engine = innodb                                                                 |
+----------+------------+----------------------------------------------------------------------------------------------------+
5 rows in set, 1 warning (0.00 sec)
```

---
## Задание 4

Изучите файл my.cnf в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб
Приведите в ответе измененный файл my.cnf.

### Ответ:
```bash
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/

innodb_flush_method = O_DSYN
innodb_file_per_table = 1
innodb_log_buffer_size = 1M
innodb_buffer_pool_size = 1G
innodb_log_file_size = 100M
```
