## Домашнее задание к занятию «Базовые объекты K8S»
----
### Задание 1. Создать Pod с именем hello-world
Создать манифест (yaml-конфигурацию) Pod.
```bash
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: myapp
  name: hello-world
  namespace: default
spec:
  containers:
    - image: gcr.io/kubernetes-e2e-test-images/echoserver:2.2
      imagePullPolicy: IfNotPresent
      name: echoserver
      ports:
        - containerPort: 8080
          name: http-web-svc
```
Использовать image - gcr.io/kubernetes-e2e-test-images/echoserver:2.2.
Подключиться локально к Pod с помощью kubectl port-forward и вывести значение (curl или в браузере).
```bash
admin@k8s:~$ kubectl apply -f ./src/pod.yml
pod/hello-world created

admin@k8s:~$ kubectl port-forward --address 0.0.0.0 -n default pod/hello-world 3000:8080
Forwarding from 0.0.0.0:3000 -> 8080
```
```bash
admin@k8s:~$ kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
hello-world    1/1     Running   0          15m
```
<img width="724" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/92d31400-b976-43ea-a702-a0a2a2958fb3">

### Задание 2. Создать Service и подключить его к Pod
Создать Pod с именем netology-web.
```bash
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: myapp
  name: netology-web
  namespace: default
spec:
  containers:
    - image: gcr.io/kubernetes-e2e-test-images/echoserver:2.2
      imagePullPolicy: IfNotPresent
      name: echoserver
      ports:
        - containerPort: 8080
          name: http-web-svc
```
```bash
admin@k8s:~$ kubectl apply -f ./src/pod.yml
```
Использовать image — gcr.io/kubernetes-e2e-test-images/echoserver:2.2.
Создать Service с именем netology-svc и подключить к netology-web.
```bash
apiVersion: v1
kind: Service
metadata:
  name: netology-svc
spec:
  ports:
    - name: web
      port: 80
      protocol: TCP
      targetPort: http-web-svc
  selector:
    app: myapp
```
```bash
admin@k8s:~$ kubectl apply -f ./src/service.yml
service/netology-svc created
```
```bash
admin@k8s:~$ kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
netology-web   1/1     Running   0          21m
hello-world    1/1     Running   0          15m
```
Подключиться локально к Service с помощью kubectl port-forward и вывести значение (curl или в браузере).
```bash
admin@k8s:~$ kubectl port-forward --address 0.0.0.0 -n default svc/netology-svc 3000:80
Forwarding from 0.0.0.0:3000 -> 8080
```
<img width="668" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/eb0723df-da10-40d9-acd7-bee7f2d6ee55">

