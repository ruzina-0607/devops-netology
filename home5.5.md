Задача 1
-------------------
Дайте письменые ответы на следующие вопросы:

1) В чём отличие режимов работы сервисов в Docker Swarm кластере: replication и global?
2) Какой алгоритм выбора лидера используется в Docker Swarm кластере?
3) Что такое Overlay Network?

Ответ: 
1) Если использовать replicated, то задается количество экземпляров этого сервиса. Далее Docker Swarm сам решает, какие из доступных worker этих сервисов задеплоить. Если использовать тип global, то всегда будет разворачиваться по одному экземпляру на каждую доступную в кластере ноду.
2) Алгоритм RAFT - алгоритм построен на распределенном консенсусе, то есть в единицу времени. Как минимум участвуют две ноды: отправляют заявку на лидерство, тот, кто первый ответил, становится лидером. Дальше в работе ноды между собой посылают запросы, чтобы определить доступен ли лидер и отвечает ли он до сих пор самый первый. В случае когда лидер не ответил в заданное время, идет пересогласование по тому же принципу. 
3) Overlay Network - распределенная сеть кластера, которая позволяет общаться контейнерам между собой на разных нодах (возможно шифрование трафика). Docker engine в рамках такой сети сам занимается маршрутизацией.

Задача 2
--------------
Создать ваш первый Docker Swarm кластер в Яндекс.Облаке

Ответ:
```bash
[root@node01 ~]# docker node ls
ID                            HOSTNAME                STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
n0r9e4a9h7ogszerh959s2gr8 *   node01.netology.cloud   Ready     Active         Leader           20.10.22
sjnwyn8scx0ycoanhmwk5let5     node02.netology.yc      Ready     Active         Reachable        20.10.22
ialc3ptdizkfv8jpp8jjpca1n     node03.netology.yc      Ready     Active         Reachable        20.10.22
rm6uaz8ap8ec4k8bpap5k4xrj     node04.netology.yc      Ready     Active                          20.10.22
chyiqfqtfo8df30izuj3axidt     node05.netology.yc      Ready     Active                          20.10.22
rm4menbz1mmy4cinxev27s8o4     node06.netology.yc      Ready     Active                          20.10.22
```

Задача 3
-------------------
Создать ваш первый, готовый к боевой эксплуатации кластер мониторинга, состоящий из стека микросервисов.

Ответ:
```bash
[root@node01 ~]# docker service ls
ID             NAME                                MODE         REPLICAS   IMAGE                                          PORTS
ca11pvcjzpyn   swarm_monitoring_alertmanager       replicated   1/1        stefanprodan/swarmprom-alertmanager:v0.14.0
7e98c6cltrrb   swarm_monitoring_caddy              replicated   1/1        stefanprodan/caddy:latest                      *:3000->3000/tcp, *:9090->9090/tcp, *:9093-9094->9093-9094/tcp
wya53tejts01   swarm_monitoring_cadvisor           global       6/6        google/cadvisor:latest
oqy598gcez4i   swarm_monitoring_dockerd-exporter   global       6/6        stefanprodan/caddy:latest
60zem4m8oscj   swarm_monitoring_grafana            replicated   1/1        stefanprodan/swarmprom-grafana:5.3.4
xwc32i3n28rj   swarm_monitoring_node-exporter      global       6/6        stefanprodan/swarmprom-node-exporter:v0.16.0
rw15sz74l4ew   swarm_monitoring_prometheus         replicated   1/1        stefanprodan/swarmprom-prometheus:v2.5.0
3n3gkvx0at8u   swarm_monitoring_unsee              replicated   1/1        cloudflare/unsee:v0.8.0
```
