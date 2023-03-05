Домашнее задание к занятию 1 «Введение в Ansible»

------
## Подготовка к выполнению

## Установите Ansible версии 2.10 или выше.
```bash
vagrant@vagrant:~$ ansible --version
ansible [core 2.13.8]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/vagrant/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/dist-packages/ansible
  ansible collection location = /home/vagrant/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.8.10 (default, Nov 14 2022, 12:59:47) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```

## Создайте свой публичный репозиторий на GitHub с произвольным именем.
<img width="279" alt="image" src="https://user-images.githubusercontent.com/104915472/222968620-0048c530-03c1-4ce6-93ef-692cf739fd71.png">
https://github.com/ruzina-0607/devops-netology

## Скачайте Playbook из репозитория с домашним заданием и перенесите его в свой репозиторий.
https://github.com/ruzina-0607/devops-netology/tree/main/playbook

## Основная часть
## 1. Попробуйте запустить playbook на окружении из test.yml, зафиксируйте значение, которое имеет факт some_fact для указанного хоста при выполнении playbook.
```bash
vagrant@vagrant:~/home8.1/playbook$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [localhost]

TASK [Print OS] ********************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP *************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
Значение, которое имеет факт some_fact - 12

## 2. Найдите файл с переменными (group_vars), в котором задаётся найденное в первом пункте значение, и поменяйте его на all default fact.
<img width="401" alt="image" src="https://user-images.githubusercontent.com/104915472/222973768-846b0221-12e9-4eb1-a185-db0bc73efcce.png">

## 3. Воспользуйтесь подготовленным (используется docker) или создайте собственное окружение для проведения дальнейших испытаний.
## 4. Проведите запуск playbook на окружении из prod.yml. Зафиксируйте полученные значения some_fact для каждого из managed host.
## 5. Добавьте факты в group_vars каждой из групп хостов так, чтобы для some_fact получились значения: для deb — deb default fact, для el — el default fact.
## 6. Повторите запуск playbook на окружении prod.yml. Убедитесь, что выдаются корректные значения для всех хостов.
## 7. При помощи ansible-vault зашифруйте факты в group_vars/deb и group_vars/el с паролем netology.
## 8. Запустите playbook на окружении prod.yml. При запуске ansible должен запросить у вас пароль. Убедитесь в работоспособности.
## 9. Посмотрите при помощи ansible-doc список плагинов для подключения. Выберите подходящий для работы на control node.
## 10. В prod.yml добавьте новую группу хостов с именем local, в ней разместите localhost с необходимым типом подключения.
## 11. Запустите playbook на окружении prod.yml. При запуске ansible должен запросить у вас пароль. Убедитесь, что факты some_fact для каждого из хостов определены из верных group_vars.
## 12. Заполните README.md ответами на вопросы. Сделайте git push в ветку master. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым playbook и заполненным README.md.


```bash

```

---

