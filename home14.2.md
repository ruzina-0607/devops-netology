## Домашнее задание к занятию «Установка Kubernetes»
-------
### Задание 1. Установить кластер k8s с 1 master node
1. Подготовка работы кластера из 5 нод: 1 мастер и 4 рабочие ноды.
2. В качестве CRI — containerd.
3. Запуск etcd производить на мастере.
4. Способ установки выбрать самостоятельно.

ВМ мастер и воркер ноды.
<img width="921" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/a57a221f-34e7-4aab-b5ab-aa3c34b406cd">

Подготовка мастер ноды
```bash
admin@master:~$ sudo apt-get install -y apt-transport-https ca-certificates curl
```
```bash
admin@master:~$ sudo mkdir -p /etc/apt/keyrings
admin@master:~$ curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
admin@master:~$ echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main
```
```bash
admin@master:~$ sudo apt-get install -y kubelet kubeadm kubectl containerd
admin@master:~$ sudo apt-mark hold kubelet kubeadm kubectl
kubelet set on hold.
kubeadm set on hold.
kubectl set on hold.
admin@master:~$ sudo -i
root@master:~# modprobe br_netfilter
root@master:~# echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
root@master:~# echo "net.bridge.bridge-nf-call-iptables=1" >> /etc/sysctl.conf
root@master:~# echo "net.bridge.bridge-nf-call-arptables=1" >> /etc/sysctl.conf
root@master:~# echo "net.bridge.bridge-nf-call-ip6tables=1" >> /etc/sysctl.conf
root@master:~# sysctl -p /etc/sysctl.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-arptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
root@master:~# logout
```
Инициализация мастер ноды
```bash
sudo kubeadm init \
--apiserver-advertise-address=10.128.0.32 \
--pod-network-cidr 10.244.0.0/16 \
--apiserver-cert-extra-sans=158.160.108.104
```
Работоспособность мастерноды
```bash
admin@master:~$ kubectl get nodes
NAME     STATUS     ROLES           AGE   VERSION
master   Ready      control-plane   82s   v1.28.1
```
Настройка воркер ноды и присоединение к мастер
```bash
kubeadm join 10.128.0.32:6443 --token l9xjvf.8z9xl3qsaar4dvnq \
        --discovery-token-ca-cert-hash sha256:5fe105feb310df98c2c081ba0228285119a2965e23a4ebe232d3aa7f3d7cc9a1
```
Проверка
```bash
admin@master:~$ kubectl get nodes
NAME     STATUS     ROLES           AGE   VERSION
master   Ready      control-plane   27m   v1.28.1
worker1  Ready      <none>          11m   v1.28.1
```
Повтор каждой ноды и вывод:
```bash
admin@master:~$ kubectl get nodes
NAME     STATUS     ROLES           AGE   VERSION
master   Ready      control-plane   57m   v1.28.1
worker1  Ready      <none>          41m   v1.28.1
worker2  Ready      <none>          26m   v1.28.1
worker3  Ready      <none>          10m   v1.28.1
worker4  Ready      <none>          80s   v1.28.1
```
