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
NAME      STATUS   ROLES           AGE     VERSION
master    Ready    control-plane   5m53s   v1.28.1
worker1   Ready    <none>          43s     v1.28.1
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
NAME      STATUS   ROLES           AGE    VERSION
master    Ready    control-plane   11m    v1.28.1
worker1   Ready    <none>          6m5s   v1.28.1
```
Проверка deployments
