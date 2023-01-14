Домашнее задание к занятию "12. Инфраструктура как код"

------
## Задание 1

Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?
Будет ли центральный сервер для управления инфраструктурой?
Будут ли агенты на серверах?
Будут ли использованы средства для управления конфигурацией или инициализации ресурсов?
Какие инструменты из уже используемых вы хотели бы использовать для нового проекта?
Хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта?

### Ответ:
1) Для начала - гибридный режим с переводом на неизменяемый тип инфраструктуры. Будем использовать Ansible + Terraform 
для определения необходимых компонентов и конфигурации. Далее когда релизы станут более стабильными, можем перейти на Packer + Terraform + Docker + Kubernetes.
2) Да. Это позволит отказаться от агентов на конечных хостах, что упростит процесс мониторинга, логирования, предоставления доступов другим администраторам, разработчикам.
3) Нет
4) Будем использовать Ansible + Terraform. В дальнейшем полностью перейдем на использование средств инициализации ресурсов.
5) Инструменты:
Packer - для создания образов
Terraform - для управления инфраструктурой
Docker - для контейнеризации приложений
Kebernetes - для оркестрации контейнеризированных приложений
Ansible - для управления конфигурациями
Teamcity - автоматизация процессов CI/CD
6) Мониторинг Prometheus + Node Exporter + Grafana

----
## Задача 2. Установка терраформ.

Установите терраформ при помощи менеджера пакетов используемого в вашей операционной системе. 
В виде результата этой задачи приложите вывод команды terraform --version.

### Ответ:
```bash
vagrant@vagrant:~$ curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK
vagrant@vagrant:~$ sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
H
sudo apt-get update && sudo apt-get install terraform
```
```bash
vagrant@vagrant:~$ sudo terraform --version
Terraform v1.3.7
on linux_amd64
```

---
## Задача 3. Поддержка легаси кода.

В какой-то момент вы обновили терраформ до новой версии, например с 0.12 до 0.13. А код одного из проектов настолько устарел, 
что не может работать с версией 0.13. В связи с этим необходимо сделать так, чтобы вы могли одновременно использовать последнюю версию терраформа 
установленную при помощи штатного менеджера пакетов и устаревшую версию 0.12.
В виде результата этой задачи приложите вывод --version двух версий терраформа доступных на вашем компьютере или виртуальной машине.

### Ответ:
```bash
vagrant@vagrant:~$ sudo mkdir -p /usr/local/tf/0.12
vagrant@vagrant:~$ cd /usr/local/tf/0.12
vagrant@vagrant:/usr/local/tf/0.12$ sudo wget https://releases.hashicorp.com/terraform/0.12.31/terraform_0.12.31_linux_amd64.zip
vagrant@vagrant:/usr/local/tf/0.12$ sudo unzip terraform_0.12.31_linux_amd64.zip
Archive:  terraform_0.12.31_linux_amd64.zip
  inflating: terraform
vagrant@vagrant:/usr/local/tf/0.12$ sudo rm terraform_0.12.31_linux_amd64.zip
vagrant@vagrant:/usr/local/tf/0.12$ sudo ln -s /usr/local/tf/0.12/terraform /usr/bin/terraform12
vagrant@vagrant:/usr/local/tf/0.12$ sudo chmod +x /usr/bin/terraform12
```
```bash
vagrant@vagrant:/usr/local/tf/0.12$ terraform12 --version
Terraform v0.12.31

Your version of Terraform is out of date! The latest version
is 1.3.7. You can update by downloading from https://www.terraform.io/downloads.html
vagrant@vagrant:/usr/local/tf/0.12$ sudo terraform --version
Terraform v1.3.7
on linux_amd64
```
---
