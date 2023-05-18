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
<img width="506" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/90c548a9-469e-46e7-9fc9-4df1ef8f841a">

2. Скачайте пакет sonar-scanner, который вам предлагает скачать SonarQube.
```bash
 wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
 
 unzip sonar-scanner-cli-4.8.0.2856-linux.zip
 ```
3. Сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
```bash
vagrant@vagrant:~/home9.3/infrastructure/sonar-scanner-4.8.0.2856-linux/bin$ export PATH=$(pwd):$PATH
```
4. Проверьте sonar-scanner --version.
```bash
vagrant@vagrant:~/home9.3/infrastructure$ sonar-scanner --version
INFO: Scanner configuration file: /home/vagrant/home9.3/infrastructure/sonar-scanner-4.8.0.2856-linux/conf/sonar-scanner.properties
INFO: Project root configuration file: /home/vagrant/home9.3/infrastructure/sonar-project.properties
INFO: SonarScanner 4.8.0.2856
INFO: Java 11.0.17 Eclipse Adoptium (64-bit)
INFO: Linux 5.4.0-136-generic amd64
```
5. Запустите анализатор против кода из директории example с дополнительным ключом -Dsonar.coverage.exclusions=fail.py.
```bash
vagrant@vagrant:~/home9.3/example$ sonar-scanner \
>   -Dsonar.projectKey=net \
>   -Dsonar.sources=. \
>   -Dsonar.host.url=http://158.160.34.65:9000 \
>   -Dsonar.login=aa9d7e8406365aac97eddc191ca6ba8b94622c90 \
> -Dsonar.coverage.exclusions=fail.py

INFO: EXECUTION SUCCESS
INFO: ------------------------------------------------------------------------
```
6. Посмотрите результат в интерфейсе.
<img width="803" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/b7dbc64d-ef1b-49e7-be0c-79e9b033d2ce">

7. Исправьте ошибки, которые он выявил, включая warnings.
```bash
def increment(index):
    index += 1
    return index
def get_square(numb):
    return numb*numb
def print_numb(numb):
    print("Number is {}".format(numb))

index = 0
while (index < 10):
    index = increment(index)
    print(get_square(index))
```
8. Запустите анализатор повторно — проверьте, что QG пройдены успешно.
9. Сделайте скриншот успешного прохождения анализа, приложите к решению ДЗ.
<img width="864" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/3e0db4b7-bb13-4afe-ba54-1ff8b0cc3ed4">


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
4. Файл maven-metadata.xml для этого артефекта:

```bash
<?xml version="1.0" encoding="UTF-8"?>
<metadata modelVersion="1.1.0">
  <groupId>netology</groupId>
  <artifactId>java</artifactId>
  <versioning>
    <latest>8_282</latest>
    <release>8_282</release>
    <versions>
      <version>8_102</version>
      <version>8_282</version>
    </versions>
    <lastUpdated>20230518214103</lastUpdated>
  </versioning>
</metadata>
```
<img width="226" alt="image" src="https://github.com/ruzina-0607/devops-netology/assets/104915472/6d70ae4b-53f8-4de2-b3c9-eb452efd426c">



## Знакомство с Maven
### Подготовка к выполнению
1. Скачайте дистрибутив с maven.
2. Разархивируйте, сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
3. Удалите из apache-maven-<version>/conf/settings.xml упоминание о правиле, отвергающем HTTP- соединение — раздел mirrors —> id: my-repository-http-unblocker.
4. Проверьте mvn --version.
```bash
vagrant@vagrant:~/home9.3/apache-maven-3.9.2$ mvn --version
Apache Maven 3.9.2 (c9616018c7a021c1c39be70fb2843d6f5f9b8a1c)
Maven home: /home/vagrant/home9.3/apache-maven-3.9.2
Java version: 11.0.19, vendor: Ubuntu, runtime: /usr/lib/jvm/java-11-openjdk-amd64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "5.4.0-136-generic", arch: "amd64", family: "unix"
```
5. Заберите директорию mvn с pom.
### Основная часть 
1. Поменяйте в pom.xml блок с зависимостями под ваш артефакт из первого пункта задания для Nexus (java с версией 8_282). Исправленный файл pom.xml:
```bash
  <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.netology.app</groupId>
  <artifactId>simple-app</artifactId>
  <version>1.0-SNAPSHOT</version>
   <repositories>
    <repository>
      <id>my-repo</id>
      <name>maven-public</name>
      <url>http://84.201.172.242:8081//repository/maven-public/</url>
    </repository>
  </repositories>
  <dependencies>
    <dependency>
      <groupId>netology</groupId>
      <artifactId>java</artifactId>
      <version>8_282</version>
      <classifier>distrib</classifier>
      <type>tar.gz</type>
    </dependency>
  </dependencies>
</project>
```
2. Запустите команду mvn package в директории с pom.xml, ожидайте успешного окончания.
```bash
  [INFO] Building jar: /home/vagrant/home9.3/mvn/target/simple-app-1.0-SNAPSHOT.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  12.710 s
```
3. Проверьте директорию ~/.m2/repository/, найдите ваш артефакт.
```bash
  -rw-rw-r-- 1 vagrant vagrant    0 May 18 23:04 java-8_282-distrib.tar.gz
-rw-rw-r-- 1 vagrant vagrant   40 May 18 23:04 java-8_282-distrib.tar.gz.sha1
-rw-rw-r-- 1 vagrant vagrant  394 May 18 23:04 java-8_282.pom.lastUpdated
-rw-rw-r-- 1 vagrant vagrant  175 May 18 23:04 _remote.repositories
```
