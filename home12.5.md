## Домашнее задание к занятию «Сетевое взаимодействие в K8S. Часть 2»
------
## Задание 1. Создать Deployment приложений backend и frontend
Создать Deployment приложения frontend из образа nginx с количеством реплик 3 шт.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
              name: nginx-80
```
Создать Deployment приложения backend из образа multitool.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: multitool
          image: wbitt/network-multitool
          env:
            - name: HTTP_PORT
              value: "8080"
          ports:
            - containerPort: 8080
              name: multitool-8080
```
Добавить Service, которые обеспечат доступ к обоим приложениям внутри кластера.
```bash
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  ports:
    - name: nginx-80
      port: 80
      protocol: TCP
      targetPort: nginx-80
  selector:
    app: frontend
```
```bash
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  ports:
    - name: multitool-8080
      port: 8080
      protocol: TCP
      targetPort: multitool-8080
  selector:
    app: backend
```
Продемонстрировать, что приложения видят друг друга с помощью Service.
Предоставить манифесты Deployment и Service в решении, а также скриншоты или вывод команды п.4.
```bash
admin@k8s:~$ kubectl apply -f ./src/frontend/deployment.yml
deployment.apps/frontend created
admin@k8s:~$ kubectl apply -f ./src/frontend/service.yml
service/frontend created
admin@k8s:~$ kubectl apply -f ./src/backend/deployment.yml
deployment.apps/backend created
admin@k8s:~$ kubectl apply -f ./src/backend/service.yml
service/backend created
```
```bash
admin@k8s:~$ kubectl get pods
NAME                               READY   STATUS    RESTARTS      AGE
frontend-69bbfb7b6d-52qt5          1/1     Running   0             46s
frontend-69bbfb7b6d-656pm          1/1     Running   0             46s
frontend-69bbfb7b6d-8d592          1/1     Running   0             46s
backend-75b975f87d-2pcwg           1/1     Running   0             28s
backend-75b975f87d-r5spq           1/1     Running   0             28s
backend-75b975f87d-vntjq           1/1     Running   0             28s
```
```bash
admin@k8s:~$ kubectl exec -it backend-75b975f87d-2pcwg -- curl frontend:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
## Задание 2. Создать Ingress и обеспечить доступ к приложениям снаружи кластера
Включить Ingress-controller в MicroK8S.
Создать Ingress, обеспечивающий доступ снаружи по IP-адресу кластера MicroK8S так, чтобы при запросе только по адресу открывался frontend а при добавлении /api - backend.
Продемонстрировать доступ с помощью браузера или curl с локального компьютера.
Предоставить манифесты и скриншоты или вывод команды п.2.
