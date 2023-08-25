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
  replicas: 2
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
Создать Service, который обеспечит доступ до реплик приложений из п.1.
Создать отдельный Pod с приложением multitool и убедиться с помощью curl, что из пода есть доступ до приложений из п.1.
#### Задание 2. Создать Deployment и обеспечить старт основного контейнера при выполнении условий
Создать Deployment приложения nginx и обеспечить старт контейнера только после того, как будет запущен сервис этого приложения.
Убедиться, что nginx не стартует. В качестве Init-контейнера взять busybox.
Создать и запустить Service. Убедиться, что Init запустился.
Продемонстрировать состояние пода до и после запуска сервиса.
