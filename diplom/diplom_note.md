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
Убедитесь, что теперь вы можете выполнить команды terraform destroy и terraform apply без дополнительных ручных действий.
В случае использования Terraform Cloud в качестве backend убедитесь, что применение изменений успешно проходит, используя web-интерфейс Terraform cloud.

key.json
main.tf








3. Запустить и сконфигурировать Kubernetes кластер.
4. Установить и настроить систему мониторинга.
5. Настроить и автоматизировать сборку тестового приложения с использованием Docker-контейнеров.
6. Настроить CI для автоматической сборки и тестирования.
7. Настроить CD для автоматического развёртывания приложения.
