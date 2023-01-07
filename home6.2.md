# Домашнее задание к занятию "6.2. SQL"

------

## Задание 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, в который будут складываться данные БД и бэкапы.
Приведите получившуюся команду или docker-compose манифест.

### Ответ:
```bash
root@server1:/home/vagrant# docker pull postgres:12
12: Pulling from library/postgres
025c56f98b67: Pull complete
26dc25c16f4e: Pull complete
a032d8a894de: Pull complete
40dba7d35750: Pull complete
8ebb44a56070: Pull complete
813fd6cf203b: Pull complete
7024f61bf8f5: Pull complete
23f986b322e8: Pull complete
2ea53cc53a00: Pull complete
f6513efd6ed7: Pull complete
946bdd08f546: Pull complete
219e7aa178ac: Pull complete
1a29c4b8415a: Pull complete
Digest: sha256:10dbdea0299264e845e73e77c8f7c09b570cc610a30d17b1b09887feecfcc575
Status: Downloaded newer image for postgres:12
docker.io/library/postgres:12
```
```bash
root@server1:/home/vagrant# docker volume create vol2
vol2
```
```bash
root@server1:/home/vagrant# docker volume create vol1
vol1
```
```bash
root@server1:/home/vagrant# docker run --rm --name pg-docker -e POSTGRES_PASSWORD=postgres -ti -p 5432:5432 -v vol1:/var/lib/postgresql/data -v vol2:/var/lib/postgresql postgres:12
```
```bash
vagrant@vagrant:/$ sudo docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
8aefbd67ef30   postgres:12   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   pg-docker
```

Какие значения переменным c,d,e будут присвоены? Почему?

| Переменная  | Значение | Обоснование |
| ------------- | ------------- | ------------- |
| `c`  | ???  | ??? |
| `d`  | ???  | ??? |
| `e`  | ???  | ??? |

----

## Задание 2

На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным (после чего скрипт должен завершиться). В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```bash
while ((1==1)
do
	curl https://localhost:4757
	if (($? != 0))
	then
		date >> curl.log
	fi
done
```

### Ваш скрипт:
```bash
???
```

---

## Задание 3

Необходимо написать скрипт, который проверяет доступность трёх IP: `192.168.0.1`, `173.194.222.113`, `87.250.250.242` по `80` порту и записывает результат в файл `log`. Проверять доступность необходимо пять раз для каждого узла.

### Ваш скрипт:
```bash
???
```

---
## Задание 4

Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается.

### Ваш скрипт:
```bash
???
```

---
