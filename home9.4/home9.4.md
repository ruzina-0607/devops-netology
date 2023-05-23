Домашнее задание к занятию 10 «Jenkins»

------
## Подготовка к выполнению
1. Создать два VM: для jenkins-master и jenkins-agent.
2. Установить Jenkins при помощи playbook.
3. Запустить и проверить работоспособность.
4. Сделать первоначальную настройку.


## Основная часть 
Сделать Freestyle Job, который будет запускать molecule test из любого вашего репозитория с ролью.
Сделать Declarative Pipeline Job, который будет запускать molecule test из любого вашего репозитория с ролью.
Перенести Declarative Pipeline в репозиторий в файл Jenkinsfile.
Создать Multibranch Pipeline на запуск Jenkinsfile из репозитория.
Создать Scripted Pipeline, наполнить его скриптом из pipeline.
Внести необходимые изменения, чтобы Pipeline запускал ansible-playbook без флагов --check --diff, если не установлен параметр при запуске джобы (prod_run = True). По умолчанию параметр имеет значение False и запускает прогон с флагами --check --diff.
Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозиторий в файл ScriptedJenkinsfile.
Отправить ссылку на репозиторий с ролью и Declarative Pipeline и Scripted Pipeline.
