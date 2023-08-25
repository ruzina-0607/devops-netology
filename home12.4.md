## Домашнее задание к занятию «Сетевое взаимодействие в K8S. Часть 1»
-----
### Задание 1. Создать Deployment и обеспечить доступ к контейнерам приложения по разным портам из другого Pod внутри кластера
Создать Deployment приложения, состоящего из двух контейнеров (nginx и multitool), с количеством реплик 3 шт.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-multitool
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
              name: nginx-80
        - name: multitool
          image: wbitt/network-multitool
          env:
            - name: HTTP_PORT
              value: "8080"
          ports:
            - containerPort: 8080
              name: multitool-8080
```
Создать Service, который обеспечит доступ внутри кластера до контейнеров приложения из п.1 по порту 9001 — nginx 80, по 9002 — multitool 8080.
```bash
apiVersion: v1
kind: Service
metadata:
  name: netology-svc
spec:
  ports:
    - name: nginx-80
      port: 9001
      protocol: TCP
      targetPort: nginx-80
    - name: multitool-8080
      port: 9002
      protocol: TCP
      targetPort: multitool-8080
  selector:
    app: nginx
```
Создать отдельный Pod с приложением multitool и убедиться с помощью curl, что из пода есть доступ до приложения из п.1 по разным портам в разные контейнеры.
```bash
apiVersion: v1
kind: Pod
metadata:
  name: netology-pod
spec:
  containers:
    - image: wbitt/network-multitool
      name: multitool
      env:
        - name: HTTP_PORT
          value: "9003"
      ports:
        - containerPort: 9003
          name: multitool-9003
```
Продемонстрировать доступ с помощью curl по доменному имени сервиса.
Предоставить манифесты Deployment и Service в решении, а также скриншоты или вывод команды п.4.
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/nginx-multitool created
admin@k8s:~$ kubectl apply -f ./src/service.yml
service/netology-svc configured
admin@k8s:~$ kubectl apply -f ./src/pod.yml
pod/netology-pod created
```
```bash
admin@k8s:~$ kubectl exec -it netology-pod -- curl netology-svc:9001
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

admin@k8s:~$ kubectl exec -it netology-pod -- curl netology-svc:9002
WBITT Network MultiTool (with NGINX) - nginx-multitool-584495968d-2mnq5 - 10.1.77.21 - HTTP: 8080 , HTTPS: 443 . (Formerly praqma/network-multitool)
```
### Задание 2. Создать Service и обеспечить доступ к приложениям снаружи кластера
Создать отдельный Service приложения из Задания 1 с возможностью доступа снаружи кластера к nginx, используя тип NodePort.
```bash
apiVersion: v1
kind: Service
metadata:
  name: netology-node-port
spec:
  ports:
    - name: nginx-80
      port: 80
      protocol: TCP
      nodePort: 30080
  selector:
    app: nginx
  type: NodePort
```
```bash
admin@k8s:~$ kubectl apply -f ./src/service1.yml
service/netology-node-port created
```
Продемонстрировать доступ с помощью браузера или curl с локального компьютера.
Предоставить манифест и Service в решении, а также скриншоты или вывод команды п.2.
```bash
admin@k8s:~$ curl http://62.84.118.225:30080
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
