## Домашнее задание к занятию «Организация сети»
-----
### Задание 1. Yandex Cloud

Создать пустую VPC. Выбрать зону.
### Публичная подсеть.
Создать в VPC subnet с названием public, сетью 192.168.10.0/24.
Создать в этой подсети NAT-инстанс, присвоив ему адрес 192.168.10.254. В качестве image_id использовать fd80mrhj8fl2oe87o4e1.
Создать в этой публичной подсети виртуалку с публичным IP, подключиться к ней и убедиться, что есть доступ к интернету.

key.json
```bash
{
   "id": "aje8r47t6dq5gvho1iou",
   "service_account_id": "ajeflrs5bqbra50su1d4",
   "created_at": "2023-01-08T00:07:30.733979461Z",
   "key_algorithm": "RSA_2048",
   "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqodq8zblg8ZW+ptweSvh\n2d4RlDX>   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqh2rzNuWDxlb6\nm3B5K>}
```
nat-instance.tf
```bash
resource "yandex_compute_instance" "nat-instance" {
  count = 1
  name  = "nat-instance-${count.index}"
  zone  = "ru-central1-a"
  allow_stopping_for_update = true
  platform_id = "standard-v2"
  hostname = "nat-instance-${count.index}"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd80mrhj8fl2oe87o4e1"
      type     = "network-hdd"
      size     = "30"
    }
  }

  network_interface {
    subnet_id  = yandex_vpc_subnet.public-subnet-a.id
    ip_address = "192.168.10.254"
    nat        = true
  }

  metadata = {
    ssh-keys = "debian:${file("~/.ssh/id_ed25519.pub")}"
  }

  scheduling_policy {
    preemptible = true
  }
}
```
network.tf
```bash
resource "yandex_vpc_network" "example_network" {
    name = "example_network"
}

resource "yandex_vpc_subnet" "public-subnet-a" {
    name           = "public"
    zone           = "ru-central1-a"
    network_id     = yandex_vpc_network.example_network.id
    v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_vpc_route_table" "routing_table" {
    network_id = yandex_vpc_network.example_network.id

    static_route {
        destination_prefix = "0.0.0.0/0"
        next_hop_address = "192.168.10.254"
    }
}

resource "yandex_vpc_subnet" "private-subnet-a" {
    name           = "private"
    zone           = "ru-central1-a"
    network_id     = yandex_vpc_network.example_network.id
    route_table_id = yandex_vpc_route_table.routing_table.id
    v4_cidr_blocks = ["192.168.20.0/24"]
}
```
output.tf
```bash
output "nat-instance_external_ip_address" {
  value = yandex_compute_instance.nat-instance.*.network_interface.0.nat_ip_address
}

output "public-instance_external_ip_address" {
  value = yandex_compute_instance.public-instance.*.network_interface.0.nat_ip_address
}

output "public-instance_iternal_ip_address" {
  value = yandex_compute_instance.public-instance.*.network_interface.0.ip_address
}

output "private-instance_iternal_ip_address" {
  value = yandex_compute_instance.private-instance.*.network_interface.0.ip_address
}
```
private_vps.tf
```bash
resource "yandex_compute_instance" "private-instance" {
  count = 1
  name  = "private-${count.index}"
  zone  = "ru-central1-a"
  allow_stopping_for_update = true
  platform_id = "standard-v2"
  hostname = "private-${count.index}"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8oshj0osht8svg6rfs"
      type     = "network-hdd"
      size     = "30"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.private-subnet-a.id
    nat       = false
  }

  metadata = {
    ssh-keys = "debian:${file("~/.ssh/id_ed25519.pub")}"
  }

  scheduling_policy {
    preemptible = true
  }
}
```
provider.tf
```bash
# Provider
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
}
```
public_vps.tf
```bash
resource "yandex_compute_instance" "public-instance" {
  count = 1
  name  = "public-${count.index}"
  zone  = "ru-central1-a"
  allow_stopping_for_update = true
  platform_id = "standard-v2"
  hostname = "public-${count.index}"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8oshj0osht8svg6rfs"
      type     = "network-hdd"
      size     = "30"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.public-subnet-a.id
    nat       = true
  }

  metadata = {
    ssh-keys = "debian:${file("~/.ssh/id_ed25519.pub")}"
  }

  scheduling_policy {
    preemptible = true
  }
}
```
variables.tf
```bash
variable "yandex_cloud_id" {
  default = "b1g5ctemf2eqma8gi6gi"
}

variable "yandex_folder_id" {
  default = "b1gin0fiqua9csbdg9so"
}
```
Далее выполняем terraform apply и устанавливаем traceroute
```bash
vagrant@vagrant:~/terraform1$ terraform init
...
vagrant@vagrant:~/terraform1$ terraform plan
...
vagrant@vagrant:~/terraform1$ terraform apply
...
```
<img width="912" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/b584df68-68d9-4a1c-a247-597d0846cb7d">

```bash
vagrant@vagrant:~/terraform1$ ssh debian@51.250.65.196
debian@public-0:~$ sudo apt-get update
debian@public-0:~$ sudo apt-get install traceroute
```
Проверка
```bash
debian@public-0:~$ traceroute ya.ru
traceroute to ya.ru (77.88.55.242), 30 hops max, 60 byte packets
 1  * * *
 2  * * *
 3  * * *
 4  * * *
 5  sas-32z3-ae1.yndx.net (87.250.239.183)  10.472 ms 10.302 ms 10.132 ms
 6  * * *
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
### Приватная подсеть.
Создать в VPC subnet с названием private, сетью 192.168.20.0/24.
Создать route table. Добавить статический маршрут, направляющий весь исходящий трафик private сети в NAT-инстанс.
Создать в этой приватной подсети виртуалку с внутренним IP, подключиться к ней через виртуалку, созданную ранее, и убедиться, что есть доступ к интернету.
```bash
vagrant@vagrant:~/terraform1$ scp -i ~/.ssh/id_ed25519 ~/.ssh/id_ed25519 debian@51.250.65.196:.ssh/id_ed25519
id_ed25519
vagrant@vagrant:~/terraform1$ ssh debian@51.250.65.196
debian@public-0:~/.ssh$ ssh debian@192.168.20.4

debian@private-0:~$ sudo apt-get update
debian@private-0:~$ sudo apt-get install traceroute
```
Проверка
```bash
debian@private-0:~$ traceroute ya.ru
traceroute to ya.ru (77.88.55.242), 30 hops max, 60 byte packets
 1  192.168.20.1 (192.168.20.1)  0.474 ms  0.472 ms  0.485 ms
 2  * * *
 3  nat-instance-0.ru-central1.internal (192.168.10.254)  1.194 ms  1.142 ms  1.124 ms
 4  nat-instance-0.ru-central1.internal (192.168.10.254)  1.144 ms  1.126 ms  1.113 ms
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  sas-32z1-ae2.yndx.net (87.250.239.179)  4.668 ms  5.491 ms  11.192 ms
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
