Домашнее задание к занятию "13. Облачные провайдеры и синтаксис Terraform."

------
## Задание 1

Файл main.tf

```bash
provider "yandex" {
  cloud_id  = "b1g5ctemf2eqma8gi6gi"
  folder_id = "b1gin0fiqua9csbdg9so"
  zone      = "ru-central1-a"
}

resource "yandex_compute_instance" "vm-1" {
  name = "terraform2"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8f32s6camma9729vqa"
          name        = "centos-7-base"
      type        = "network-nvme"
      size        = "40"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

}

resource "yandex_vpc_network" "network-1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
    zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "internal_ip_address_vm_1" {
  value = yandex_compute_instance.vm-1.network_interface.0.ip_address
}

output "external_ip_address_vm_1" {
  value = yandex_compute_instance.vm-1.network_interface.0.nat_ip_address
}
```
Файл versions.tf
```bash
terraform {
 required_providers {
   yandex = {
     source  = "yandex-cloud/yandex"
   }
 }
 required_version = ">= 0.13"
}
```
Сервисный аккаунт
<img width="361" alt="image" src="https://user-images.githubusercontent.com/104915472/212491441-c2f7ed49-0480-4bdd-bfc5-731b3e702ed5.png">
Образ
<img width="853" alt="image" src="https://user-images.githubusercontent.com/104915472/212491661-c11ec667-ecb5-4b85-8f13-ae5715e6e901.png">
Токен
```bash
vagrant@vagrant:~/terraform2$ export YC_TOKEN=`yc iam create-token`
```
Инициализация
```bash
vagrant@vagrant:~/terraform2$ terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of yandex-cloud/yandex from the dependency lock file
- Using previously-installed yandex-cloud/yandex v0.84.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```
Применение конфигурации
```bash
vagrant@vagrant:~/terraform2$ terraform apply -auto-approve

Outputs:

external_ip_address_vm_1 = "51.250.9.145"
internal_ip_address_vm_1 = "192.168.10.26"
```
Plan (сделала замену на новые данные)
```bash
vagrant@vagrant:~/terraform2$ terraform plan
yandex_vpc_network.network-1: Refreshing state... [id=enpsip0287pa8lpdnm55]
yandex_vpc_subnet.subnet-1: Refreshing state... [id=e9bu1d15to8fvleob86f]
yandex_compute_instance.vm-1: Refreshing state... [id=fhmnqcrh5s08ogs3pspv]

Terraform used the selected providers to generate the following execution plan. Resource actions are
indicated with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # yandex_compute_instance.vm-1 must be replaced
-/+ resource "yandex_compute_instance" "vm-1" {
      ~ created_at                = "2023-01-14T19:02:16Z" -> (known after apply)
      ~ folder_id                 = "b1gin0fiqua9csbdg9so" -> (known after apply)
      ~ fqdn                      = "fhmnqcrh5s08ogs3pspv.auto.internal" -> (known after apply)
      + hostname                  = (known after apply)
      ~ id                        = "fhmnqcrh5s08ogs3pspv" -> (known after apply)
      - labels                    = {} -> null
      - metadata                  = {} -> null
        name                      = "terraform2"
      + service_account_id        = (known after apply)
      ~ status                    = "running" -> (known after apply)
      ~ zone                      = "ru-central1-a" -> (known after apply)
        # (2 unchanged attributes hidden)

      ~ boot_disk {
          ~ device_name = "fhmo8km8lg00jo98c7vk" -> (known after apply)
          ~ disk_id     = "fhmo8km8lg00jo98c7vk" -> (known after apply)
          ~ mode        = "READ_WRITE" -> (known after apply)
            # (1 unchanged attribute hidden)

          ~ initialize_params {
              ~ block_size  = 4096 -> (known after apply)
              + description = (known after apply)
                name        = "centos-7-base"
              + snapshot_id = (known after apply)
              ~ type        = "network-ssd" -> "network-nvme" # forces replacement
                # (2 unchanged attributes hidden)
            }
        }

      ~ metadata_options {
          ~ aws_v1_http_endpoint = 1 -> (known after apply)
          ~ aws_v1_http_token    = 1 -> (known after apply)
          ~ gce_http_endpoint    = 1 -> (known after apply)
          ~ gce_http_token       = 1 -> (known after apply)
        }

      ~ network_interface {
          ~ index              = 0 -> (known after apply)
          ~ ip_address         = "192.168.10.9" -> (known after apply)
          ~ ipv6               = false -> (known after apply)
          + ipv6_address       = (known after apply)
          ~ mac_address        = "d0:0d:17:d3:37:12" -> (known after apply)
          ~ nat_ip_address     = "51.250.68.36" -> (known after apply)
          ~ nat_ip_version     = "IPV4" -> (known after apply)
          ~ security_group_ids = [] -> (known after apply)
            # (3 unchanged attributes hidden)
        }

      ~ placement_policy {
          ~ host_affinity_rules = [] -> (known after apply)
          + placement_group_id  = (known after apply)
        }

      ~ resources {
          - gpus          = 0 -> null
            # (3 unchanged attributes hidden)
        }

      ~ scheduling_policy {
          ~ preemptible = false -> (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.

Changes to Outputs:
  ~ external_ip_address_vm_1 = "51.250.68.36" -> (known after apply)
  ~ internal_ip_address_vm_1 = "192.168.10.9" -> (known after apply)

──────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these
actions if you run "terraform apply" now.
```
Ответ на вопрос: при помощи какого инструмента (из разобранных на прошлом занятии) можно создать свой образ ami?
Amazon Web Services CloudFormation

---
