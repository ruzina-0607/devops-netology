## Дипломный практикум в Yandex.Cloud
----
### Задание 1 Подготовить облачную инфраструктуру на базе облачного провайдера Яндекс.Облако.
### Создание облачной инфраструктуры
Для начала необходимо подготовить облачную инфраструктуру в ЯО при помощи Terraform.

Создайте сервисный аккаунт, который будет в дальнейшем использоваться Terraform для работы с инфраструктурой с необходимыми и достаточными правами. Не стоит использовать права суперпользователя.

<img width="288" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/142ffa79-f995-4f65-96e4-17d7495e6de4">

Создание статического ключа. Статический ключ доступа необходим для аутентификации сервисного аккаунта в AWS-совместимых API.

<img width="601" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/791ae80f-bc98-489c-8eca-3098cdc33129">

```bash
vagrant@vagrant:~/terraform1$ yc iam key create --service-account-name terraform -o terraform.json --folder-id b1gin0fiqua9csbdg9so

vagrant@vagrant:~/terraform1$ yc config set service-account-key terraform.json
```

Подготовьте backend для Terraform:

б. Альтернативный вариант: S3 bucket в созданном ЯО аккаунте

<img width="469" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/206a5707-e206-4b06-8497-e5fa954c0a82">

backend.tf
```bash
# backend.tf
terraform {
  backend "s3" {
    endpoint = "storage.yandexcloud.net"
    bucket   = "bucket-tf-diplom"
    key        = "diplom/terraform.tfstate"
    region     = "ru-central1-a"
    access_key = "YCAJEoUsNJdWSbYu******"
    secret_key = "YCPfCVAvKUrYvBw2iQCdwv*******"
    skip_region_validation      = true
    skip_credentials_validation = true
  }
}
```

Настройте workspaces

а. Рекомендуемый вариант: создайте два workspace: stage и prod. В случае выбора этого варианта все последующие шаги должны учитывать факт существования нескольких workspace.
```bash
vagrant@vagrant:~/terraform1$ terraform init

Initializing the backend...
Do you want to copy existing state to the new backend?
  Pre-existing state was found while migrating the previous "local" backend to the
  newly configured "s3" backend. No existing state was found in the newly
  configured "s3" backend. Do you want to copy this state to the new "s3"
  backend? Enter "yes" to copy and "no" to start with an empty state.

  Enter a value: yes


Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Reusing previous version of yandex-cloud/yandex from the dependency lock file
- Using previously-installed yandex-cloud/yandex v0.84.0

Terraform has made some changes to the provider dependency selections recorded
in the .terraform.lock.hcl file. Review those changes and commit them to your
version control system if they represent changes you intended to make.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

vagrant@vagrant:~/terraform1$ terraform workspace new stage && terraform workspace new prod
Created and switched to workspace "stage"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
Created and switched to workspace "prod"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
```
Создайте VPC с подсетями в разных зонах доступности.

networks.tf
```bash
# networks.tf
# Create ya.cloud VPC
resource "yandex_vpc_network" "k8s-network" {
  name = "ya-network"
}
# Create ya.cloud public subnet
resource "yandex_vpc_subnet" "k8s-network-a" {
  name           = "public-a"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.k8s-network.id
  v4_cidr_blocks = ["172.28.0.0/24"]
}
resource "yandex_vpc_subnet" "k8s-network-b" {
  name           = "public-b"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.k8s-network.id
  v4_cidr_blocks = ["172.28.10.0/24"]
}
resource "yandex_vpc_subnet" "k8s-network-c" {
  name           = "public-c"
  zone           = "ru-central1-c"
  network_id     = yandex_vpc_network.k8s-network.id
  v4_cidr_blocks = ["172.28.20.0/24"]
}
```
main.tf
```bash
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = ">=0.67.0"
    }
  }
}

provider "yandex" {
  token = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
}
```
variables.tf
```bash
variable "yc_token" {
  default = "y0_AgAAAA*****"
}
variable "yc_cloud_id" {
  default = "b1g5ctemf2e*******"
}
variable "yc_folder_id" {
  default = "b1gin0fiqua*******"
}
variable "sa_id" {
  default = "aje6l3j29i******"
}
```
Убедитесь, что теперь вы можете выполнить команды terraform destroy и terraform apply без дополнительных ручных действий.
```bash
vagrant@vagrant:~/terraform1$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # yandex_vpc_network.k8s-network will be created
  + resource "yandex_vpc_network" "k8s-network" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "ya-network"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_subnet.k8s-network-a will be created
  + resource "yandex_vpc_subnet" "k8s-network-a" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "public-a"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "172.28.0.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-a"
    }

  # yandex_vpc_subnet.k8s-network-b will be created
  + resource "yandex_vpc_subnet" "k8s-network-b" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "public-b"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "172.28.10.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-b"
    }

  # yandex_vpc_subnet.k8s-network-c will be created
  + resource "yandex_vpc_subnet" "k8s-network-c" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "public-c"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "172.28.20.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-c"
    }

Plan: 4 to add, 0 to change, 0 to destroy.

Do you want to perform these actions in workspace "prod"?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

yandex_vpc_network.k8s-network: Creating...
yandex_vpc_network.k8s-network: Creation complete after 3s [id=enp9du2it1rq7cdvatru]
yandex_vpc_subnet.k8s-network-a: Creating...
yandex_vpc_subnet.k8s-network-c: Creating...
yandex_vpc_subnet.k8s-network-b: Creating...
yandex_vpc_subnet.k8s-network-a: Creation complete after 0s [id=e9bf8voroic14r6jsaif]
yandex_vpc_subnet.k8s-network-b: Creation complete after 1s [id=e2ldsqmebb4s378mgogq]
yandex_vpc_subnet.k8s-network-c: Creation complete after 1s [id=b0ck5j1j0ohmqdue2ght]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```
<img width="603" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/b5520be5-9132-40cc-8b46-bdf9b39d4b4d">

<img width="454" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/6166a4e6-c611-4c3b-a09d-66e8ff96f756">

<img width="498" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/fe4e25ba-d5b1-41bc-8e74-63ecb5d65e9a">

### Задание 2. Запустить и сконфигурировать Kubernetes кластер.
На этом этапе необходимо создать Kubernetes кластер на базе предварительно созданной инфраструктуры. Требуется обеспечить доступ к ресурсам из Интернета.

2. Альтернативный вариант: воспользуйтесь сервисом Yandex Managed Service for Kubernetes

  а. С помощью terraform resource для kubernetes создать региональный мастер kubernetes с размещением нод в разных 3 подсетях
  
  б. С помощью terraform resource для kubernetes node group

master.tf
```bash
resource "yandex_kubernetes_cluster" "k8s-yandex" {
  name        = "k8s-yandex"
  description = "description"

  network_id = "${yandex_vpc_network.k8s-network.id}"

  master {
    regional {
      region = "ru-central1"

      location {
        zone      = "${yandex_vpc_subnet.k8s-network-a.zone}"
        subnet_id = "${yandex_vpc_subnet.k8s-network-a.id}"
      }

      location {
        zone      = "${yandex_vpc_subnet.k8s-network-b.zone}"
        subnet_id = "${yandex_vpc_subnet.k8s-network-b.id}"
      }

      location {
        zone      = "${yandex_vpc_subnet.k8s-network-c.zone}"
        subnet_id = "${yandex_vpc_subnet.k8s-network-c.id}"
      }
    }
   version   = "1.27"
    public_ip = true
}

  service_account_id      = "aje8e05gurp8q3fnb49a"
  node_service_account_id = "ajen2su57142gfu5i0av"
  labels = {
    my_key       = "my_value"
    my_other_key = "my_other_value"
  }

  release_channel = "STABLE"
  network_policy_provider = "CALICO"
}
```
nodes.tf
```bash
resource "yandex_kubernetes_node_group" "mynodes" {
  cluster_id  = "${yandex_kubernetes_cluster.k8s-yandex.id}"
  name        = "mynodes"
  description = "description"
  version     = "1.27"

  labels = {
    "key" = "value"
  }

  instance_template {
    platform_id = "standard-v2"

    network_interface {
      nat                = true
      subnet_ids = [yandex_vpc_subnet.k8s-network-a.id]
    }

    resources {
      memory = 8
      cores  = 4
    }

    boot_disk {
      type = "network-hdd"
      size = 64
    }

    scheduling_policy {
      preemptible = false
    }

  }

  scale_policy {
    auto_scale {
      min = 3
      max = 6
      initial = 3
    }
  }

  allocation_policy {
    location {
      zone = "ru-central1-a"
    }
  }
}
```
outputs.tf
```bash
output "cluster_external_v4_endpoint" {
  value = yandex_kubernetes_cluster.k8s-yandex.master.0.external_v4_endpoint
}

output "cluster_id" {
  value = yandex_kubernetes_cluster.k8s-yandex.id
}
output "registry_id" {
  description = "registry ID"
  value=yandex_container_registry.diplom.id
}
```
sa.tf 
```bash
resource "yandex_iam_service_account" "terra" {
  folder_id = "b1gin0fiqua9csbdg9so"
  name  = "terra"
}

resource "yandex_iam_service_account" "puller" {
  folder_id = "b1gin0fiqua9csbdg9so"
  name  = "puller"
}

// Grant permissions
resource "yandex_resourcemanager_folder_iam_member" "terra-editor" {
  folder_id = "b1gin0fiqua9csbdg9so"
  role  = "editor"
  member  = "serviceAccount:${yandex_iam_service_account.terra.id}"
}

resource "yandex_container_registry_iam_binding" "puller" {
  registry_id = "${yandex_container_registry.diplom.id}"
  role        = "editor"
  members = ["serviceAccount:${yandex_iam_service_account.puller.id}"]
}
```
Команда terraform apply
```bash
vagrant@vagrant:~/terraform1$ terraform apply
yandex_iam_service_account.puller: Refreshing state... [id=aje52atqdp1rbfrdct8m]
yandex_iam_service_account.terra: Refreshing state... [id=ajetuohibvqmdj0bn10s]
yandex_vpc_network.k8s-network: Refreshing state... [id=enp9du2it1rq7cdvatru]
yandex_container_registry.diplom: Refreshing state... [id=crp385jqto57425qjvc1]
yandex_resourcemanager_folder_iam_member.terra-editor: Refreshing state... [id=b1gin0fiqua9csbdg9so/editor/serviceAccount:ajetuohibvqmdj0bn10s]
yandex_container_registry_iam_binding.puller: Refreshing state... [id=crp385jqto57425qjvc1/editor]
yandex_vpc_subnet.k8s-network-c: Refreshing state... [id=b0ck5j1j0ohmqdue2ght]
yandex_vpc_subnet.k8s-network-a: Refreshing state... [id=e9bf8voroic14r6jsaif]
yandex_vpc_subnet.k8s-network-b: Refreshing state... [id=e2ldsqmebb4s378mgogq]
yandex_kubernetes_cluster.k8s-yandex: Refreshing state... [id=catf7lqjt4gbmqn8k736]
yandex_kubernetes_node_group.mynodes: Refreshing state... [id=cato5kjiq5u9bv5qdmo6]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are
needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

cluster_external_v4_endpoint = "https://158.160.59.43"
cluster_id = "catf7lqjt4gbm***"
registry_id = "crp385jqto574****"
```
Создание конфигурации
```bash
vagrant@vagrant:~/terraform1$ yc managed-kubernetes cluster get-credentials --id $(terraform output -json cluster_id | s
ed 's/\"//g') --external

Context 'yc-k8s-yandex' was added as default to kubeconfig '/home/vagrant/.kube/config'.
Check connection to cluster using 'kubectl cluster-info --kubeconfig /home/vagrant/.kube/config'.

Note, that authentication depends on 'yc' and its config profile 'default'.
To access clusters using the Kubernetes API, please use Kubernetes Service Account.
```
Ожидаемый результат:

Работоспособный Kubernetes кластер.
В файле ~/.kube/config находятся данные для доступа к кластеру.
```bash
vagrant@vagrant:~/terraform1$ cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: *********************
    server: https://158.160.59.43
  name: yc-managed-k8s-catf7lqjt4gbmqn8k736
contexts:
- context:
    cluster: yc-managed-k8s-catf7lqjt4gbmqn8k736
    user: yc-managed-k8s-catf7lqjt4gbmqn8k736
  name: yc-k8s-yandex
current-context: yc-k8s-yandex
kind: Config
preferences: {}
users:
- name: yc-managed-k8s-catf7lqjt4gbmqn8k736
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args:
      - k8s
      - create-token
      - --profile=default
      command: /home/vagrant/yandex-cloud/bin/yc
      env: null
      provideClusterInfo: false
```
Команда kubectl get pods --all-namespaces отрабатывает без ошибок.
```bash
vagrant@vagrant:~/terraform1$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                                  READY   STATUS      RESTARTS      AGE
kube-system   calico-node-82n6x                                     1/1     Running     0             22h
kube-system   calico-node-gx5ws                                     1/1     Running     0             22h
kube-system   calico-node-k44fm                                     1/1     Running     0             22h
kube-system   calico-typha-564fff4699-m8g5m                         1/1     Running     0             22h
kube-system   calico-typha-horizontal-autoscaler-7d7cf6b5f9-xn8z9   1/1     Running     0             22h
kube-system   calico-typha-vertical-autoscaler-7f784b789d-7czrl     1/1     Running     3 (22h ago)   22h
kube-system   coredns-f4696fd9f-j62zh                               1/1     Running     1 (22h ago)   23h
kube-system   coredns-f4696fd9f-zp2m4                               1/1     Running     0             22h
kube-system   ip-masq-agent-996kb                                   1/1     Running     0             22h
kube-system   ip-masq-agent-cjv9l                                   1/1     Running     0             22h
kube-system   ip-masq-agent-xzzgt                                   1/1     Running     0             22h
kube-system   kube-dns-autoscaler-bd7cc5977-l4pkn                   1/1     Running     0             22h
kube-system   kube-proxy-77kn6                                      1/1     Running     0             22h
kube-system   kube-proxy-8zkb7                                      1/1     Running     0             22h
kube-system   kube-proxy-vcqtv                                      1/1     Running     0             22h
kube-system   metrics-server-6f485d9c99-2mrrn                       2/2     Running     0             22h
kube-system   npd-v0.8.0-chqtt                                      1/1     Running     0             22h
kube-system   npd-v0.8.0-srg2s                                      1/1     Running     0             22h
kube-system   npd-v0.8.0-x585h                                      1/1     Running     0             22h
kube-system   yc-disk-csi-node-v2-2259m                             6/6     Running     0             22h
kube-system   yc-disk-csi-node-v2-bgl4d                             6/6     Running     0             22h
kube-system   yc-disk-csi-node-v2-q6ghk                             6/6     Running     0             22h
```
### Задание 3. Создание тестового приложения
Для перехода к следующему этапу необходимо подготовить тестовое приложение, эмулирующее основное приложение разрабатываемое вашей компанией.

Способ подготовки:

Рекомендуемый вариант:

а. Создайте отдельный git репозиторий с простым nginx конфигом, который будет отдавать статические данные.

б. Подготовьте Dockerfile для создания образа приложения.

Создание Dockerfile с простым nginx, который отдает статическую страницу c именем хоста(контейнера) и версией сборки(тэгом).

Dockerfile
```bash
FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/
COPY index.html /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;"]
```
Файл конфигурации default.conf
```bash
server {
    listen       80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
    ssi on;
}
```
index.html
```bash
<html>
<body>
        <h1>Host: <!--#echo var="HOSTNAME" --></h1>
        Version: 1.1
</body>
</html>
```
Сборка образа и отправка его в registry DockerHub
```bash
vagrant@vagrant:~/terraform1$ docker build -t ruzina/nginx:0.1 .
[+] Building 1.1s (8/8) FINISHED
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 170B                                                                               0.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [internal] load metadata for docker.io/library/nginx:alpine                                                    1.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 63B                                                                                   0.0s
 => [1/3] FROM docker.io/library/nginx:alpine@sha256:16164a43b5faec40adb521e98272edc528e74f31c1352719132b8f7e5341  0.0s
 => CACHED [2/3] COPY default.conf /etc/nginx/conf.d/                                                              0.0s
 => CACHED [3/3] COPY index.html /usr/share/nginx/html/                                                            0.0s
 => exporting to image                                                                                             0.0s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:d8ec7c1fc5904db887fde775f1b1002215838173ce5a4507cfcafc9bedb870f5                       0.0s
 => => naming to docker.io/ruzina/nginx:0.1

vagrant@vagrant:~/terraform1$ sudo docker push ruzina/nginx:0.1
The push refers to repository [docker.io/ruzina/nginx]
1fd591ed815b: Pushed
0c0398cd167d: Pushed
ef6182113153: Mounted from library/nginx
4236627f761b: Mounted from library/nginx
993cbb8cb4db: Mounted from library/nginx
2cf6da0936ad: Mounted from library/nginx
ca660b07329b: Mounted from library/nginx
854831065e8f: Mounted from library/nginx
1adf0aa7b921: Mounted from library/nginx
4693057ce236: Mounted from library/nginx
0.1: digest: sha256:0fc47af0621394ea3b063d1f98489f3f2d44bfc544743e369d57c57bce01847b size: 2403
```
Ожидаемый результат:

Git репозиторий с тестовым приложением и Dockerfile.
Регистр с собранным docker image. В качестве регистра может быть DockerHub или Yandex Container Registry, созданный также с помощью terraform.

<img width="948" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/ff0bab6c-53d8-4b6f-888b-362f8d77e6a1">

```bash
vagrant@vagrant:~/terraform1$ docker run -d --rm -p 80:80 --name nginx ruzina/nginx:0.1
e2bf81f70279e6838769e73c9fa7c8d4ebd82a81ae6ccc7126d9112232598331

vagrant@vagrant:~/terraform1$ curl localhost
<html>
<body>
        <h1>Host: e2bf81f70279</h1>
        Version: 1.1
</body>
</html>
```

4. Установить и настроить систему мониторинга.
5. Настроить CI для автоматической сборки и тестирования.
6. Настроить CD для автоматического развёртывания приложения.
