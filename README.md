# Blogicum - это тестовый проект на платформе Яндекс Практикум  

#### В четвертой части проекта мы научились работать CBV. Создавать формы и пагинацию. 

#### Так же научились создавать миксины и настраивать админку 

#### Стэк который я использовал в этом проекте: 

- Python3.11 

- Django3.2

- Sqlite2.8.17 


## Установить репозиторий по `ssh`: 

```sh 

git clone git@github.com:ipoderator/django_sprint4.git 

``` 

### Создать вирутальное `окружение`: 

```sh 

python3.11 -m venv venv 

``` 

 

### Активировать виртуальное `окружение`: 

```sh 

. ./venv/bin/activate 

``` 

 

### Установить `зависимости`: 

```sh 

pip install -r requirements.txt 

``` 

 

### Установить `миграции`: 

```sh 

python3.11 manage.py migrate 

``` 

 

### Запустить `проект`: 

```sh 

./manage.py runserver 

``` 

 

### Создать суперпользователя  

```sh 

python3.11 manage.py createsuperuser 

``` 

 

### После создания моделей сделать миграции и ипортировать данные из json в db. 

```sh 

python3.11 manage.py loaddata db.json  

``` 