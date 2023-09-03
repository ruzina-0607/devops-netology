## Домашнее задание к занятию «Как работает сеть в K8s»
-----
### Задание 1. Создать сетевую политику или несколько политик для обеспечения доступа
Создать deployment'ы приложений frontend, backend и cache и соответсвующие сервисы.
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: app
  labels:
    app: frontend
spec:
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: wbitt/network-multitool
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: app
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: app
  labels:
    app: backend
spec:
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: wbitt/network-multitool
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: app
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cache
  namespace: app
  labels:
    app: cache
spec:
  selector:
    matchLabels:
      app: cache
  template:
    metadata:
      labels:
        app: cache
    spec:
      containers:
        - name: cache
          image: wbitt/network-multitool
---
apiVersion: v1
kind: Service
metadata:
  name: cache-service
  namespace: app
spec:
  selector:
    app: cache
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```
В качестве образа использовать network-multitool.
Разместить поды в namespace App.
```bash
admin@k8s:~$ kubectl create namespace app
namespace/app created

admin@k8s:~$ kubectl apply -f ./frontdeploy.yml
deployment.apps/frontend created
service/frontend-service created

admin@k8s:~$ kubectl apply -f ./backdeploy.yml
deployment.apps/backend created
service/backend-service created

admin@k8s:~$ kubectl apply -f ./cachedeploy.yml
deployment.apps/cache created
service/cache-service created
```
```bash
admin@k8s:~$ kubectl get all -n app
NAME                            READY   STATUS    RESTARTS   AGE
pod/frontend-84577d7d6d-g289g   1/1     Running   0          2m21s
pod/backend-778ff4c6b6-pkzvt    1/1     Running   0          2m2s
pod/cache-67655b9854-9jllh      1/1     Running   0          114s

NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/frontend-service   ClusterIP   10.152.183.118   <none>        80/TCP    2m21s
service/backend-service    ClusterIP   10.152.183.184   <none>        80/TCP    2m2s
service/cache-service      ClusterIP   10.152.183.172   <none>        80/TCP    114s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/frontend   1/1     1            1           2m22s
deployment.apps/backend    1/1     1            1           2m2s
deployment.apps/cache      1/1     1            1           114s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/frontend-84577d7d6d   1         1         1       2m21s
replicaset.apps/backend-778ff4c6b6    1         1         1       2m2s
replicaset.apps/cache-67655b9854      1         1         1       114s
```
Создать политики, чтобы обеспечить доступ frontend -> backend -> cache. Другие виды подключений должны быть запрещены.
```bash
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-deny-all
  namespace: app
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
  policyTypes:
  - Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-cache
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: cache
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
  policyTypes:
  - Ingress
```
Продемонстрировать, что трафик разрешён и запрещён.
```bash
admin@k8s:~$ time kubectl exec -ti -n app frontend-84577d7d6d-g289g -- curl backend-service
WBITT Network MultiTool (with NGINX) - backend-778ff4c6b6-pkzvt - 10.1.77.62 - HTTP: 80 , HTTPS: 443 . (Formerly praqma/network-multitool)

real    0m0.116s
user    0m0.048s
sys     0m0.020s
admin@k8s:~$ time kubectl exec -ti -n app frontend-84577d7d6d-g289g -- curl cache-service
^Ccommand terminated with exit code 130

real    0m4.811s
user    0m0.057s
sys     0m0.013s
admin@k8s:~$ time kubectl exec -ti -n app backend-778ff4c6b6-pkzvt -- curl cache-service
WBITT Network MultiTool (with NGINX) - cache-67655b9854-9jllh - 10.1.77.39 - HTTP: 80 , HTTPS: 443 . (Formerly praqma/network-multitool)

real    0m0.120s
user    0m0.051s
sys     0m0.018s
admin@k8s:~$ time kubectl exec -ti -n app backend-778ff4c6b6-pkzvt -- curl frontend-service
^Ccommand terminated with exit code 130

real    0m1.311s
user    0m0.056s
sys     0m0.014s
admin@k8s:~$ time kubectl exec -ti -n app cache-67655b9854-9jllh -- curl frontend-service
^Ccommand terminated with exit code 130

real    0m1.538s
user    0m0.062s
sys     0m0.010s
admin@k8s:~$ time kubectl exec -ti -n app cache-67655b9854-9jllh -- curl backend-service
^Ccommand terminated with exit code 130

real    0m2.590s
user    0m0.055s
sys     0m0.014s
```
