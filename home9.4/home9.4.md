Домашнее задание к занятию 10 «Jenkins»

------
## Подготовка к выполнению
1. Создать два VM: для jenkins-master и jenkins-agent.
<img width="903" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/077fa57d-cbfd-494d-8a87-b4ecd1d742d7">

2. Установить Jenkins при помощи playbook.
3. Запустить и проверить работоспособность.
4. Сделать первоначальную настройку.
<img width="664" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/c74af3c7-4757-41f9-85cf-c063911a3c1f">
<img width="708" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/441c34a4-211d-472c-b590-822fde6b4515">


## Основная часть 
1. Сделать Freestyle Job, который будет запускать molecule test из любого вашего репозитория с ролью.
2. Сделать Declarative Pipeline Job, который будет запускать molecule test из любого вашего репозитория с ролью.
3. Перенести Declarative Pipeline в репозиторий в файл Jenkinsfile.
4. Создать Multibranch Pipeline на запуск Jenkinsfile из репозитория.
5. Создать Scripted Pipeline, наполнить его скриптом из pipeline.
6. Внести необходимые изменения, чтобы Pipeline запускал ansible-playbook без флагов --check --diff, если не установлен параметр при запуске джобы (prod_run = True). По умолчанию параметр имеет значение False и запускает прогон с флагами --check --diff.
7. Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозиторий в файл ScriptedJenkinsfile.
8. Отправить ссылку на репозиторий с ролью и Declarative Pipeline и Scripted Pipeline.
