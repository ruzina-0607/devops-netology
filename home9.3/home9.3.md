Домашнее задание к занятию 9 «Процессы CI/CD»

------
## Подготовка к выполнению
1. Создайте два VM в Yandex Cloud с параметрами: 2CPU 4RAM Centos7 (остальное по минимальным требованиям).
<img width="903" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/84cca36f-881a-4c29-83e4-e7868fa70a1d">

2. Пропишите в inventory playbook созданные хосты.
```bash
all:
  hosts:
    sonar-01:
      ansible_host: 158.160.34.65
    nexus-01:
      ansible_host: 84.201.172.242
  children:
    sonarqube:
      hosts:
        sonar-01:
    nexus:
      hosts:
        nexus-01:
    postgres:
      hosts:
        sonar-01:
  vars:
    ansible_connection_type: paramiko
    ansible_user: admin
```
3. Добавьте в files файл со своим публичным ключом (id_rsa.pub). Если ключ называется иначе — найдите таску в плейбуке, которая использует id_rsa.pub имя, и исправьте на своё.
```bash
  - name: "Set up ssh key to access for managed node"
      authorized_key:
        user: "{{ sonarqube_db_user }}"
        state: present
        key: "{{ lookup('file', '/home/vagrant/.ssh/id_ed25519.pub') }}"
```
4. Запустите playbook, ожидайте успешного завершения.
<img width="657" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/b978fedd-a03b-43ec-a204-9875431fd36b">

5. Проверьте готовность SonarQube через браузер.
6. Зайдите под admin\admin, поменяйте пароль на свой.
<img width="597" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/6f9f9b49-543b-47e5-8c24-d8efca35df40">

7. Проверьте готовность Nexus через бразуер.
8. Подключитесь под admin\admin123, поменяйте пароль, сохраните анонимный доступ.
<img width="953" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/daca49ee-0ec1-4d48-bbbe-e1fd11a017e8">


## Знакомоство с SonarQube
### Основная часть
1. Создайте новый проект, название произвольное.
2. Скачайте пакет sonar-scanner, который вам предлагает скачать SonarQube.
3. Сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
4. Проверьте sonar-scanner --version.
5. Запустите анализатор против кода из директории example с дополнительным ключом -Dsonar.coverage.exclusions=fail.py.
6. Посмотрите результат в интерфейсе.
7. Исправьте ошибки, которые он выявил, включая warnings.
8. Запустите анализатор повторно — проверьте, что QG пройдены успешно.
9. Сделайте скриншот успешного прохождения анализа, приложите к решению ДЗ.

## Знакомство с Nexus
### Основная часть
1. В репозиторий maven-public загрузите артефакт с GAV-параметрами:
- groupId: netology;
- artifactId: java;
- version: 8_282;
- classifier: distrib;
- type: tar.gz.
2. В него же загрузите такой же артефакт, но с version: 8_102.
3. Проверьте, что все файлы загрузились успешно.
4. В ответе пришлите файл maven-metadata.xml для этого артефекта.

## Знакомство с Maven
### Подготовка к выполнению
1. Скачайте дистрибутив с maven.
2. Разархивируйте, сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
3. Удалите из apache-maven-<version>/conf/settings.xml упоминание о правиле, отвергающем HTTP- соединение — раздел mirrors —> id: my-repository-http-unblocker.
4. Проверьте mvn --version.
5. Заберите директорию mvn с pom.
### Основная часть 
1. Поменяйте в pom.xml блок с зависимостями под ваш артефакт из первого пункта задания для Nexus (java с версией 8_282).
2. Запустите команду mvn package в директории с pom.xml, ожидайте успешного окончания.
3. Проверьте директорию ~/.m2/repository/, найдите ваш артефакт.
4. В ответе пришлите исправленный файл pom.xml.
