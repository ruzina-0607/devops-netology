## Домашнее задание к занятию «Kubernetes. Причины появления. Команда kubectl»
-------
### Задание 1. Установка MicroK8S
Установить MicroK8S на локальную машину или на удалённую виртуальную машину.
```bash
admin@k8s:~$ sudo microk8s version
MicroK8s v1.27.4 revision 5643
```
Установить dashboard.
```bash
admin@k8s:~$ sudo microk8s enable dashboard

admin@k8s:~$ sudo microk8s status -a dashboard
enabled
```
Сгенерировать сертификат для подключения к внешнему ip-адресу.
```bash
admin@k8s:~$ sudo microk8s refresh-certs --cert front-proxy-client.crt
Taking a backup of the current certificates under /var/snap/microk8s/5643/certs-backup/
Creating new certificates
Signature ok
subject=CN = front-proxy-client
Getting CA Private Key
Restarting service kubelite.
```
### Задание 2. Установка и настройка локального kubectl
Установить на локальную машину kubectl.
```bash
admin@k8s:~$ kubectl version --output=json
{
  "clientVersion": {
    "major": "1",
    "minor": "28",
    "gitVersion": "v1.28.1",
    "gitCommit": "8dc49c4b984b897d423aab4971090e1879eb4f23",
    "gitTreeState": "clean",
    "buildDate": "2023-08-24T11:23:10Z",
    "goVersion": "go1.20.7",
    "compiler": "gc",
    "platform": "linux/amd64"
  },
  "kustomizeVersion": "v5.0.4-0.20230601165947-6ce0bf390ce3"
}
```
Настроить локально подключение к кластеру.
```bash
admin@k8s:~/.kube$ kubectl get nodes
NAME   STATUS   ROLES    AGE   VERSION
k8s    Ready    <none>   20m   v1.27.4
```
Подключиться к дашборду с помощью port-forward.
```bash
admin@k8s:~$ kubectl port-forward --address 0.0.0.0 -n kube-system service/kubernetes-dashboard 10443:443
```
<img width="960" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/1eed9e0e-34ba-4b45-89dd-b809851628fc">


