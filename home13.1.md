## Домашнее задание к занятию «Хранение в K8s. Часть 1»
------
### Задание 1
Создать Deployment приложения, состоящего из двух контейнеров и обменивающихся данными.

1. Создать Deployment приложения, состоящего из контейнеров busybox и multitool.
2. Сделать так, чтобы busybox писал каждые пять секунд в некий файл в общей директории.
3. Обеспечить возможность чтения файла контейнером multitool.
4. Продемонстрировать, что multitool может читать файл, который периодоически обновляется.
5. Предоставить манифесты Deployment в решении, а также скриншоты или вывод команды из п. 4.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multitool-busybox
  labels:
    app: common
spec:
  replicas: 1
  selector:
    matchLabels:
      app: common
  template:
    metadata:
      labels:
        app: common
    spec:
      containers:
        - name: multitool
          image: wbitt/network-multitool
          volumeMounts:
            - name: vol
              mountPath: /input
        - name: busybox
          image: busybox:latest
          command: [ 'sh', '-c', 'while true; do echo Done >> /output/done.txt; sleep 5; done' ]
          volumeMounts:
            - name: vol
              mountPath: /output
      volumes:
        - name: vol
          hostPath:
            path: /var/data
```
```bash
admin@k8s:~$ kubectl apply -f ./src/deployment.yml
deployment.apps/multitool-busybox created
admin@k8s:~$ kubectl get pods
NAME                                READY   STATUS    RESTARTS        AGE
multitool-busybox-5ddfdf74c5-t5krv   2/2    Running      0            18s
```
```bash
admin@k8s:~$ kubectl exec -it multitool-busybox-5ddfdf74c5-t5krv -- cat /input/done.txt
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
```
```bash
admin@k8s:~$ kubectl exec -it multitool-busybox-5ddfdf74c5-t5krv -- cat /input/done.txt
Defaulted container "multitool" out of: multitool, busybox
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
Done
```
### Задание 2
Создать DaemonSet приложения, которое может прочитать логи ноды.

1. Создать DaemonSet приложения, состоящего из multitool.
2. Обеспечить возможность чтения файла /var/log/syslog кластера MicroK8S.
3. Продемонстрировать возможность чтения файла изнутри пода.
4. Предоставить манифесты Deployment, а также скриншоты или вывод команды из п. 2.
```bash
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: multitool
  labels:
    app: common
spec:
  selector:
    matchLabels:
      app: common
  template:
    metadata:
      labels:
        app: common
    spec:
      containers:
        - name: multitool
          image: wbitt/network-multitool:latest
          volumeMounts:
            - name: log
              mountPath: /log
      volumes:
        - name: log
          hostPath:
            path: /var/log
#            path: /var/log/syslog
#            path: /var/log/test.log
#            type: File
```
```bash
admin@k8s:~$ kubectl apply -f ./src/DaemonSet.yml
daemonset.apps/multitool created

admin@k8s:~$ kubectl get daemonset
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
multitool   1         1         1       1            1           <none>          6s

admin@k8s:~$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS       AGE
multitool-tvhjz                      1/1     Running   0              33s
```
```bash
admin@k8s:~$ kubectl exec -it multitool-tvhjz -- ls -la log
total 3164
drwxrwxr-x   11 root     113           4096 Aug 25 19:39 .
drwxr-xr-x    1 root     root          4096 Aug 25 23:46 ..
-rw-r--r--    1 root     root          6676 Aug 24 18:35 alternatives.log
drwxr-xr-x    2 root     root          4096 Aug 24 18:35 apt
-rw-r-----    1 107      adm         224590 Aug 25 23:46 auth.log
-rw-r-----    1 107      adm            534 Aug 24 17:56 auth.log.1
-rw-rw----    1 root     43          194304 Aug 25 23:46 btmp
-rw-r-----    1 root     adm           8299 Aug 25 19:40 cloud-init-output.log
-rw-r-----    1 107      adm         239498 Aug 25 19:40 cloud-init.log
drwxr-xr-x    2 root     root         12288 Aug 25 23:46 containers
drwxr-xr-x    2 root     root          4096 Feb 10  2023 dist-upgrade
-rw-r-----    1 root     adm          77205 Aug 25 19:39 dmesg
-rw-r-----    1 root     adm          78077 Aug 24 17:56 dmesg.0
-rw-r--r--    1 root     root          4112 Aug 24 18:35 dpkg.log
drwxr-x---    4 root     adm           4096 Aug 17 16:29 installer
drwxr-sr-x    4 root     nginx         4096 Aug 24 17:56 journal
-rw-r-----    1 107      adm         106161 Aug 25 23:46 kern.log
-rw-r-----    1 107      adm          91905 Aug 24 17:56 kern.log.1
drwxr-xr-x    2 111      117           4096 Aug 24 17:58 landscape
-rw-rw-r--    1 root     43          292292 Aug 25 22:10 lastlog
drwxr-xr-x   22 root     root          4096 Aug 25 23:46 pods
drwx------    2 root     root          4096 Feb 17  2023 private
-rw-r-----    1 107      adm        1956070 Aug 25 23:47 syslog
-rw-r-----    1 107      adm         129080 Aug 24 17:56 syslog.1
-rw-r--r--    1 root     root          5346 Aug 25 20:18 ubuntu-advantage.log
drwxr-x---    2 root     adm           4096 Aug 24 18:34 unattended-upgrades
-rw-rw-r--    1 root     43            9216 Aug 25 23:31 wtmp
```
