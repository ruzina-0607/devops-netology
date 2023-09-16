## Дипломный практикум в Yandex.Cloud
----
### Задание 1
Подготовить облачную инфраструктуру на базе облачного провайдера Яндекс.Облако.
### Создание облачной инфраструктуры
Для начала необходимо подготовить облачную инфраструктуру в ЯО при помощи Terraform.

Создайте сервисный аккаунт, который будет в дальнейшем использоваться Terraform для работы с инфраструктурой с необходимыми и достаточными правами. Не стоит использовать права суперпользователя.

<img width="288" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/142ffa79-f995-4f65-96e4-17d7495e6de4">

Создание статического ключа. Статический ключ доступа необходим для аутентификации сервисного аккаунта в AWS-совместимых API.

<img width="601" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/791ae80f-bc98-489c-8eca-3098cdc33129">


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
    access_key = "YCAJEoUsNJdWSbYuW8b_B4TSp"
    secret_key = "YCPfCVAvKUrYvBw2iQCdwv6tU0h1u7NKKRx370tI"
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
  default = "b1g5ctemf2eqma8gi6gi"
}
variable "yc_folder_id" {
  default = "b1gin0fiqua9csbdg9so"
}
variable "sa_id" {
  default = "aje6l3j29i2j9h0ghjhf"
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









3. Запустить и сконфигурировать Kubernetes кластер.
4. Установить и настроить систему мониторинга.
5. Настроить и автоматизировать сборку тестового приложения с использованием Docker-контейнеров.
6. Настроить CI для автоматической сборки и тестирования.
7. Настроить CD для автоматического развёртывания приложения.
