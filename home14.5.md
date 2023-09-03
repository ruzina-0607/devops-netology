## Домашнее задание к занятию Troubleshooting
-----
## Задание
При деплое приложение web-consumer не может подключиться к auth-db. Необходимо это исправить
Установить приложение по команде:
```bash
kubectl apply -f https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml
```
Выявить проблему и описать.
Исправить проблему, описать, что сделано.
Продемонстрировать, что проблема решена.
```bash
admin@master:~$ kubectl get nodes
NAME     STATUS   ROLES           AGE     VERSION
master   Ready    control-plane   12m     v1.28.1
worker   Ready    <none>          5m59s   v1.28.1
```
```bash
admin@master:~$ kubectl apply -f https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml
Error from server (NotFound): error when creating "https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml": namespaces "web" not found
Error from server (NotFound): error when creating "https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml": namespaces "data" not found
Error from server (NotFound): error when creating "https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml": namespaces "data" not found
```
Не хватает namespace data и web:
```bash
admin@master:~$ kubectl create namespace data
namespace/data created

admin@master:~$ kubectl create namespace web
namespace/web created

admin@master:~$ kubectl apply -f https://raw.githubusercontent.com/netology-code/kuber-homeworks/main/3.5/files/task.yaml
deployment.apps/web-consumer created
deployment.apps/auth-db created
service/auth-db created
```
Проверка работоспособности кластера
```bash
admin@master:~$ kubectl get nodes
NAME     STATUS   ROLES           AGE     VERSION
master   Ready    control-plane   14m     v1.28.1
worker   Ready    <none>          8m17s   v1.28.1
```
Проверка deployments
```bash
admin@master:~$ kubectl get deployment -A
NAMESPACE     NAME           READY   UP-TO-DATE   AVAILABLE   AGE
data          auth-db        1/1     1            1           119s
kube-system   coredns        2/2     2            1           15m
web           web-consumer   2/2     2            2           119s
```
Проверка подов
```bash
admin@master:~$ kubectl get pods -A
NAMESPACE      NAME                             READY   STATUS             RESTARTS        AGE
data           auth-db-7b5cdbdc77-dk76l         1/1     Running            0               4m55s
kube-flannel   kube-flannel-ds-bwt9t            1/1     Running            0               10m
kube-flannel   kube-flannel-ds-nqzrz            1/1     Running            0               10m
kube-system    coredns-5dd5756b68-hwvws         1/1     Running            0               17m
kube-system    coredns-5dd5756b68-vmzfk         1/1     Running            0               17m
kube-system    etcd-master                      1/1     Running            0               18m
kube-system    kube-apiserver-master            1/1     Running            0               18m
kube-system    kube-controller-manager-master   1/1     Running            0               18m
kube-system    kube-proxy-f6z5c                 1/1     Running            0               17m
kube-system    kube-proxy-sb259                 1/1     Running            0               12m
kube-system    kube-scheduler-master            1/1     Running            0               18m
web            web-consumer-5f87765478-kbzc2    1/1     Running            0               4m55s
web            web-consumer-5f87765478-ns8zx    1/1     Running            0               4m55s
```
