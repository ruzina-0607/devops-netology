## Домашнее задание к занятию «Обновление приложений»
--------
### Задание 1. Выбрать стратегию обновления приложения и описать ваш выбор
Имеется приложение, состоящее из нескольких реплик, которое требуется обновить.
Ресурсы, выделенные для приложения, ограничены, и нет возможности их увеличить.
Запас по ресурсам в менее загруженный момент времени составляет 20%.
Обновление мажорное, новые версии приложения не умеют работать со старыми.
Вам нужно объяснить свой выбор стратегии обновления приложения.

Исходя из вышеперечисленного, подходит только стратегия обновления recreate. Все поды убиваются сразу и заменяются потом новыми. То есть высвобождается все пространство, и ставится новый проект. Конфликта версий не будет, проблем с пространством тоже.
Rolling не подойдет, так как там постепенно старые поды будут заменяться на новые, а условие у нас, что обновление мажорное (по этой же причине не подходят другие, например Canary, Blue/Green, Мультиверсии ...).

### Задание 2. Обновить приложение
Создать deployment приложения с контейнерами nginx и multitool. Версию nginx взять 1.19. Количество реплик — 5.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-multitool
  labels:
    app: nginx
spec:
  replicas: 5
  revisionHistoryLimit: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 5
      maxUnavailable: 20%
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
          image: nginx:1.19
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
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/nginx-multitool configured

admin@k8s:~$ kubectl get deployments
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
nginx-multitool     5/5     5            5           4d21h

admin@k8s:~$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS        AGE
nginx-multitool-585d5cc796-wsk98     2/2     Running   0               81s
nginx-multitool-585d5cc796-nb4j8     2/2     Running   0               81s
nginx-multitool-585d5cc796-z25d8     2/2     Running   0               81s
nginx-multitool-585d5cc796-qzfwc     2/2     Running   0               81s
nginx-multitool-585d5cc796-85rs8     2/2     Running   0               81s
```
Обновить версию nginx в приложении до версии 1.20, сократив время обновления до минимума. Приложение должно быть доступно.
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/nginx-multitool configured

admin@k8s:~$ kubectl get pods -w
NAME                                 READY   STATUS              RESTARTS        AGE
nginx-multitool-585d5cc796-wsk98     2/2     Running             0               4m34s
nginx-multitool-585d5cc796-nb4j8     2/2     Running             0               4m34s
nginx-multitool-585d5cc796-z25d8     2/2     Running             0               4m34s
nginx-multitool-585d5cc796-qzfwc     2/2     Running             0               4m34s
nginx-multitool-58db8cd548-4tzmj     0/2     ContainerCreating   0               5s
nginx-multitool-58db8cd548-l8tbn     0/2     ContainerCreating   0               5s
nginx-multitool-58db8cd548-68zbq     0/2     ContainerCreating   0               5s
nginx-multitool-58db8cd548-n4s6g     0/2     ContainerCreating   0               5s
nginx-multitool-58db8cd548-598d5     0/2     ContainerCreating   0               5s
nginx-multitool-58db8cd548-4tzmj     2/2     Running             0               13s
nginx-multitool-585d5cc796-nb4j8     2/2     Terminating         0               4m42s
nginx-multitool-585d5cc796-nb4j8     2/2     Terminating         0               4m45s
nginx-multitool-58db8cd548-l8tbn     2/2     Running             0               16s
nginx-multitool-585d5cc796-nb4j8     0/2     Terminating         0               4m45s
nginx-multitool-585d5cc796-z25d8     2/2     Terminating         0               4m45s
nginx-multitool-585d5cc796-z25d8     2/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-z25d8     0/2     Terminating         0               4m46s
nginx-multitool-58db8cd548-68zbq     2/2     Running             0               17s
nginx-multitool-585d5cc796-z25d8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-nb4j8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-qzfwc     2/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-nb4j8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-nb4j8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-z25d8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-z25d8     0/2     Terminating         0               4m46s
nginx-multitool-585d5cc796-qzfwc     2/2     Terminating         0               4m47s
nginx-multitool-585d5cc796-qzfwc     0/2     Terminating         0               4m47s
nginx-multitool-585d5cc796-qzfwc     0/2     Terminating         0               4m48s
nginx-multitool-585d5cc796-qzfwc     0/2     Terminating         0               4m48s
nginx-multitool-585d5cc796-qzfwc     0/2     Terminating         0               4m48s
nginx-multitool-58db8cd548-n4s6g     2/2     Running             0               19s
nginx-multitool-585d5cc796-wsk98     2/2     Terminating         0               4m48s
nginx-multitool-585d5cc796-wsk98     2/2     Terminating         0               4m49s
nginx-multitool-58db8cd548-598d5     2/2     Running             0               20s
nginx-multitool-585d5cc796-wsk98     0/2     Terminating         0               4m49s
nginx-multitool-585d5cc796-wsk98     0/2     Terminating         0               4m50s
nginx-multitool-585d5cc796-wsk98     0/2     Terminating         0               4m50s
nginx-multitool-585d5cc796-wsk98     0/2     Terminating         0               4m50s

admin@k8s:~$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS      AGE
nginx-multitool-58db8cd548-4tzmj     2/2     Running   0             4m10s
nginx-multitool-58db8cd548-l8tbn     2/2     Running   0             4m10s
nginx-multitool-58db8cd548-68zbq     2/2     Running   0             4m10s
nginx-multitool-58db8cd548-n4s6g     2/2     Running   0             4m10s
nginx-multitool-58db8cd548-598d5     2/2     Running   0             4m10s
```
Попытаться обновить nginx до версии 1.28, приложение должно оставаться доступным.
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/nginx-multitool configured
admin@k8s:~$ kubectl get pods -w
NAME                                 READY   STATUS              RESTARTS      AGE
nginx-multitool-58db8cd548-4tzmj     2/2     Running             0             5m44s
nginx-multitool-58db8cd548-l8tbn     2/2     Running             0             5m44s
nginx-multitool-58db8cd548-68zbq     2/2     Running             0             5m44s
nginx-multitool-58db8cd548-n4s6g     2/2     Running             0             5m44s
nginx-multitool-5ff69b5f6-cp7bf      0/2     ContainerCreating   0             5s
nginx-multitool-5ff69b5f6-kz86c      0/2     ContainerCreating   0             5s
nginx-multitool-5ff69b5f6-nh74m      0/2     ContainerCreating   0             5s
nginx-multitool-5ff69b5f6-hqdpl      0/2     ContainerCreating   0             4s
nginx-multitool-5ff69b5f6-lwd25      0/2     ContainerCreating   0             4s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ErrImagePull        0             16s
nginx-multitool-5ff69b5f6-kz86c      1/2     ErrImagePull        0             17s
nginx-multitool-5ff69b5f6-kz86c      1/2     ImagePullBackOff    0             18s
nginx-multitool-5ff69b5f6-nh74m      1/2     ErrImagePull        0             18s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ErrImagePull        0             18s
nginx-multitool-5ff69b5f6-nh74m      1/2     ImagePullBackOff    0             19s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ImagePullBackOff    0             19s
nginx-multitool-5ff69b5f6-lwd25      1/2     ErrImagePull        0             19s
nginx-multitool-5ff69b5f6-lwd25      1/2     ImagePullBackOff    0             20s
nginx-multitool-5ff69b5f6-kz86c      1/2     ErrImagePull        0             34s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ImagePullBackOff    0             37s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ErrImagePull        0             47s
nginx-multitool-5ff69b5f6-kz86c      1/2     ImagePullBackOff    0             48s
nginx-multitool-5ff69b5f6-nh74m      1/2     ErrImagePull        0             50s
nginx-multitool-5ff69b5f6-lwd25      1/2     ErrImagePull        0             50s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ImagePullBackOff    0             60s
nginx-multitool-5ff69b5f6-nh74m      1/2     ImagePullBackOff    0             63s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ErrImagePull        0             63s
nginx-multitool-5ff69b5f6-lwd25      1/2     ImagePullBackOff    0             64s
nginx-multitool-5ff69b5f6-kz86c      1/2     ErrImagePull        0             65s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ImagePullBackOff    0             74s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ErrImagePull        0             75s
nginx-multitool-5ff69b5f6-nh74m      1/2     ErrImagePull        0             78s
nginx-multitool-5ff69b5f6-lwd25      1/2     ErrImagePull        0             78s
nginx-multitool-5ff69b5f6-kz86c      1/2     ImagePullBackOff    0             80s
nginx-multitool-5ff69b5f6-nh74m      1/2     ImagePullBackOff    0             90s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ImagePullBackOff    0             89s
nginx-multitool-5ff69b5f6-lwd25      1/2     ImagePullBackOff    0             91s
nginx-multitool-5ff69b5f6-kz86c      1/2     ErrImagePull        0             114s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ErrImagePull        0             114s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ErrImagePull        0             117s
nginx-multitool-5ff69b5f6-kz86c      1/2     ImagePullBackOff    0             2m6s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ImagePullBackOff    0             2m9s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ImagePullBackOff    0             2m11s
nginx-multitool-5ff69b5f6-lwd25      1/2     ErrImagePull        0             2m12s
nginx-multitool-5ff69b5f6-nh74m      1/2     ErrImagePull        0             2m13s
nginx-multitool-5ff69b5f6-lwd25      1/2     ImagePullBackOff    0             2m24s
nginx-multitool-5ff69b5f6-nh74m      1/2     ImagePullBackOff    0             2m27s

admin@k8s:~kubectl get pods
NAME                                 READY   STATUS             RESTARTS      AGE
nginx-multitool-58db8cd548-4tzmj     2/2     Running            0             8m44s
nginx-multitool-58db8cd548-l8tbn     2/2     Running            0             8m44s
nginx-multitool-58db8cd548-68zbq     2/2     Running            0             8m44s
nginx-multitool-58db8cd548-n4s6g     2/2     Running            0             8m44s
nginx-multitool-5ff69b5f6-kz86c      1/2     ImagePullBackOff   0             3m5s
nginx-multitool-5ff69b5f6-cp7bf      1/2     ImagePullBackOff   0             3m5s
nginx-multitool-5ff69b5f6-hqdpl      1/2     ImagePullBackOff   0             3m4s
nginx-multitool-5ff69b5f6-lwd25      1/2     ImagePullBackOff   0             3m4s
nginx-multitool-5ff69b5f6-nh74m      1/2     ImagePullBackOff   0             3m5s
```
Откатиться после неудачного обновления.
```bash
admin@k8s:~$ kubectl rollout history deployment/nginx-multitool
deployment.apps/nginx-multitool
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
4         <none>

admin@k8s:~$ kubectl rollout undo deployment/nginx-multitool
deployment.apps/nginx-multitool rolled back

admin@k8s:~$ kubectl rollout history deployment/nginx-multitool
deployment.apps/nginx-multitool
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
4         <none>
5         <none>

admin@k8s:~$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS      AGE
nginx-multitool-58db8cd548-4tzmj     2/2     Running   0             13m
nginx-multitool-58db8cd548-l8tbn     2/2     Running   0             13m
nginx-multitool-58db8cd548-68zbq     2/2     Running   0             13m
nginx-multitool-58db8cd548-n4s6g     2/2     Running   0             13m
nginx-multitool-58db8cd548-qnfjf     2/2     Running   0             40s
```
