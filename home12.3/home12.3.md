## Домашнее задание к занятию «Запуск приложений в K8S»
--------
### Задание 1. Создать Deployment и обеспечить доступ к репликам приложения из другого Pod
Создать Deployment приложения, состоящего из двух контейнеров — nginx и multitool. Решить возникшую ошибку.
Deployment:
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-multitool
  labels:
    app: nginx
spec:
  replicas: 1
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
              value: "1180"
          ports:
            - containerPort: 1180
              name: multitool-1180
```
После запуска увеличить количество реплик работающего приложения до 2.
Продемонстрировать количество подов до и после масштабирования.
```bash
spec:
  replicas: 2
```
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/nginx-multitool created
```
```bash
admin@k8s:~$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
nginx-multitool   2/2     2            2           21s
```
```bash
admin@k8s:~$ kubectl get pods
NAME                               READY   STATUS    RESTARTS       AGE
nginx-multitool-575d684d54-5pvbs   2/2     Running   0              4m50s
```
```bash
admin@k8s:~$ kubectl get pods
NAME                               READY   STATUS    RESTARTS       AGE
nginx-multitool-575d684d54-5pvbs   2/2     Running   0              5m49s
nginx-multitool-575d684d54-vv6x9   2/2     Running   0              5m49s
```
Создать Service, который обеспечит доступ до реплик приложений из п.1.
Service:
```bash
apiVersion: v1
kind: Service
metadata:
  name: netology-svc
spec:
  ports:
    - name: nginx-80
      port: 80
      protocol: TCP
      targetPort: nginx-80
    - name: multitool-1180
      port: 1180
      protocol: TCP
      targetPort: multitool-1180
  selector:
    app: nginx
```
```bash
admin@k8s:~$ kubectl apply -f ./src/service.yml
service/netology-svc configured
```
```bash
admin@k8s:~$ kubectl get service
NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
kubernetes     ClusterIP   10.152.183.1     <none>        443/TCP           25h
netology-svc   ClusterIP   10.152.183.236   <none>        80/TCP,1180/TCP   24h
```
```bash
admin@k8s:~$ kubectl port-forward --address 0.0.0.0 -n default svc/netology-svc 3000:80
```
<img width="960" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/b406b63e-f386-427e-bb40-842ce1087d6c">
```bash
admin@k8s:~$ kubectl port-forward --address 0.0.0.0 -n default svc/netology-svc :1180
Forwarding from 0.0.0.0:46265 -> 1180
```
<img width="960" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/7ff992e1-5531-42ee-9416-5e37747abfb8">
Создать отдельный Pod с приложением multitool и убедиться с помощью curl, что из пода есть доступ до приложений из п.1.

#### Задание 2. Создать Deployment и обеспечить старт основного контейнера при выполнении условий
Создать Deployment приложения nginx и обеспечить старт контейнера только после того, как будет запущен сервис этого приложения.
Убедиться, что nginx не стартует. В качестве Init-контейнера взять busybox.
Создать и запустить Service. Убедиться, что Init запустился.
Продемонстрировать состояние пода до и после запуска сервиса.
