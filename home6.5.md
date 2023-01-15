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

```bash
vagrant@vagrant:~$ curl -X DELETE 'http://localhost:9200/ind-1?pretty'
{
  "acknowledged" : true
}
vagrant@vagrant:~$ curl -X DELETE 'http://localhost:9200/ind-2?pretty'
{
  "acknowledged" : true
}
vagrant@vagrant:~$ curl -X DELETE 'http://localhost:9200/ind-3?pretty'
{
  "acknowledged" : true
}
```

---

## Задание 3

Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.
Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
Приведите в ответе запрос API и результат вызова API для создания репозитория.
Создайте индекс test с 0 реплик и 1 шардом и приведите в ответе список индексов.
Создайте snapshot состояния кластера elasticsearch.
Приведите в ответе список файлов в директории со snapshotами.
Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.
Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.
Приведите в ответе запрос к API восстановления и итоговый список индексов.

### Ответ:
```bash
vagrant@vagrant:~$ curl -XPOST localhost:9200/_snapshot/my_cluster_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": {"location"
:"/usr/share/elasticsearch/snapshots"}}'
{
  "acknowledged" : true
}
vagrant@vagrant:~$ curl -X PUT localhost:9200/test -H 'Content-Type: applicatio
n/json' -d'{"settings": {"number_of_shards": 1, "number_of_replicas": 0}}'
{"acknowledged":true,"shards_acknowledged":true,"index":"test"}
```
```bash
vagrant@vagrant:~$ curl -X PUT localhost:9200/_snapshot/my_cluster_backup/elasticsearch?wait_for_completion=true
{"snapshot":{"snapshot":"elasticsearch","uuid":"rWFXDNoHSIC6zQDpTOc0SQ","repository":"my_cluster_backup","version_id":8060099,"version":"8.6.0","indices":[".geoip_databases","test"],"data_streams":[],"include_global_state":true,"state":"SUCCESS","start_time":"2023-01-15T16:33:14.722Z","start_time_in_millis":1673800394722,"end_time":"2023-01-15T16:33:17.357Z","end_time_in_millis":1673800397357,"duration_in_millis":2635,"failures":[],"shards":{"total":2,"failed":0,"successful":2},"feature_states":[{"feature_name":"geoip","indices":[".geoip_databases"]}]}}
```
```bash
[elasticsearch@87e6b7ded858 snapshots]$ ls -la
total 48
drwxrwxr-x 3 elasticsearch elasticsearch  4096 Jan 15 16:33 .
drwx------ 1 elasticsearch elasticsearch  4096 Jan 15 15:36 ..
-rw-rw-r-- 1 elasticsearch elasticsearch   846 Jan 15 16:33 index-0
-rw-rw-r-- 1 elasticsearch elasticsearch     8 Jan 15 16:33 index.latest
drwxrwxr-x 4 elasticsearch elasticsearch  4096 Jan 15 16:33 indices
-rw-rw-r-- 1 elasticsearch elasticsearch 18678 Jan 15 16:33 meta-rWFXDNoHSIC6zQDpTOc0SQ.dat
-rw-rw-r-- 1 elasticsearch elasticsearch   356 Jan 15 16:33 snap-rWFXDNoHSIC6zQDpTOc0SQ.dat
```
```bash
vagrant@vagrant:~$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  mMnIxz1fQ8eHVniajYu_oA   1   0          0            0       225b           225b

vagrant@vagrant:~$ curl -X GET 'http://localhost:9200/_snapshot/my_cluster_backup/*?verbose=false&pretty'
{
  "snapshots" : [
    {
      "snapshot" : "elasticsearch",
      "uuid" : "rWFXDNoHSIC6zQDpTOc0SQ",
      "repository" : "my_cluster_backup",
      "indices" : [
        ".geoip_databases",
        "test"
      ],
      "data_streams" : [ ],
      "state" : "SUCCESS"
    }
  ],
  "total" : 1,
  "remaining" : 0
}
```

---

