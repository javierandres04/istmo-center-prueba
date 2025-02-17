# Prueba Técnica - Backend - Istmo Center

## Objetivo 

Desarrollar una API RESTful para la gestión de una biblioteca digital, permitiendo a los usuarios administrar libros y préstamos. La API debe incluir autenticación, pruebas unitarias y despliegue con Docker.


## Tecnologías Utilizadas

* Django Rest Framework: Creación del API.
* PostgreSQL 14 : Base de datos.
* Docker: Configuración y despliegue del proyecto


## Estructura del proyecto

Para mantener el orden el proyecto fue dividido en distintos submódulos haciendo uso de las apps de Django estando organizadas de la siguiente manera:
- core: Cuenta con las configuraciones generales del proyecto de Django, así como también algunos archivos globales que son necesarios en otras aplicaciones. Estos se encuentran dentro de los directorios 'decorators' y 'utils'.
- users: Esta app se encarga de manejar toda la lógica relacionada con los usuarios y su autenticación. Cuenta con las rutas para la realización de operaciones CRUD sobre la tabla de usuarios (solo los administradores tienen acceso) y las rutas para autenticarse mediante JWT.
- books: Esta app se encarga de manejar toda la lógica relacionada con los libros. Cuenta con las rutas para la realización de operaciones CRUD sobre la tabla de libros y las rutas para pedir y devolver libros.

La estructura general del proyecto es la siguiente:

```
istmo-center-prueba/
├─ .gitignore
├─ django_start.sh
├─ Docker-compose.yml
├─ Dockerfile
├─ manage.py
├─ README.md
├─ requirements.txt
│
├─ books/
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ serializers/
│  │  └─ book_serializers.py
│  ├─ services/
│  │  └─book_services.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views/
│  │  ├─ book_loan_views.py
│  │  ├─ book_views.py
│  │  ├─ __init__.py
│  └─ __init__.py
│  
├─ core/
│  ├─ asgi.py
│  ├─ decorators/
│  │  └─ views_error_handling.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ utils/
│  │  ├─ base_crud_service.py
│  │  └─ paginator.py
│  └─ wsgi.py
│ 
└─ users/
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ serializers/
   │  └─ user_serializers.py
   ├─ services/
   │  └─ user_services.py
   ├─ tests.py
   ├─ urls.py
   ├─ views/
   │  └─ user_views.py
   └─ __init__.py
  
```

## Rutas disponibles: 


``` api/v1/users/ ```

Esta ruta es exclusiva para usuarios administradores.
#### Métodos:

*  GET: Devuelve una lista de usuarios paginados de la siguiente manera: 
```
{
    "total_records": 3,
    "total_pages": 1,
    "current_page": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "user@user.com",
            "name": "simple user",
            "role": "USER"
        },
        {
            "id": 2,
            "email": "user2@user.com",
            "name": "simple user",
            "role": "USER"
        },
        {
            "id": 3,
            "email": "admin@admin.com",
            "name": "",
            "role": "ADMIN"
        }
    ]
}
```
Permite paginar desde el url usando los parámetros `lmit` y `page`.

*  POST: Permite crear un usuario. Recibe los datos como JSON de la siguiente manera. PD: Sólo se pueden crear usuarios con los siguientes roles = ["ADMIN", "USER"]:

```
{
    "email": "user@user.com",
    "name": "simple user",
    "password": "default",
    "role": "USER"
}
```
Devuelve una representación JSON del objeto creado.

-------------------

``` api/v1/users/{id}/ ```

Esta ruta es exclusiva para administradores.

#### Métodos:

* GET: Devuelve el usuario que corresponda al ID solicitado.
* PUT: Permite modificar un usuario solicitado por ID, solo permite sobreescribir todos los campos del usuario. Recibe los datos en formato JSON de la siguiente manera:
```
{
    "email": "nuevomail@user.com",
    "name": "simple users",
    "password": "default1",
    "role": "USER"
}
```
Devuelve una representación JSON del objeto modificado.

* PATCH: Permite modificar uno o más atributos de un usuario solicitado por ID. Recibe los datos en formato JSON de la siguiente manera:
```
{
    "email": "nuevomail@user.com",
}
```
Devuelve una representación JSON del objeto modificado.
* DELETE: Permite eliminar un usuario solicitado por ID, devuelve una representación JSON del objeto eliminado.

-------------------

``` api/v1/register/ ```

Esta ruta se encuentra abierta a cualquier tipo de usuario, ya que es necesaria para registrase en la aplicación.

### Métodos:

* POST: Permite crear registrar un usuario en la aplicación, el usuario es creado con el rol de `USER` por defecto. Recibe los datos en formato JSON de la siguiente manera:

```
{
    "email": "newuser@user.com",
    "name": "simple users",
    "password": "default1"
}

```
Devuelve una representación JSON del objeto creado.

-------------------

``` api/v1/token/ ```

Esta ruta permite obtener un JWT de accesso y otro para refrescar el token.

### Métodos:

* POST: Recibe las credenciales del usuario en formato JSON de la siguiente manera: 

```
{
    "email": "user@user.com",
    "password": "1234",
}
```

Devuelve un objeto con el token necesario para autenticarse. Ejemplo de respuesta:

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwODQ1NiwiaWF0IjoxNzM5ODIyMDU2LCJqdGkiOiI4MTk5MzY1NzI3ZTA0YzBjOGQyZDU3NmE2MmE2Yzc4OSIsInVzZXJfaWQiOjN9.PYeGsLikiUt4L0qJfS_CgAlIExSLEcENuyDnv8omb-s",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5ODIyMzU2LCJpYXQiOjE3Mzk4MjIwNTYsImp0aSI6IjMzYTY5MDQ5YzdmYTRlMWM4OTgxZTcwNTJlMmRkODUwIiwidXNlcl9pZCI6M30.JV3fZ56Nk3fo4oVCq1UHTdyuDm6cs_DarNOmuAFBiZc"
}
```
-------------------

``` api/v1/token/refresh/ ```

Esta ruta permite refrescar un JWT previamente obtenido.

### Métodos:

* POST: Recibe el token de acceso de la siguiente manera: 

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTkwODQ1NiwiaWF0IjoxNzM5ODIyMDU2LCJqdGkiOiI4MTk5MzY1NzI3ZTA0YzBjOGQyZDU3NmE2MmE2Yzc4OSIsInVzZXJfaWQiOjN9.PYeGsLikiUt4L0qJfS_CgAlIExSLEcENuyDnv8omb-s",
}
```

Devuelve un access token renovado:

```

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5ODIyNTIwLCJpYXQiOjE3Mzk4MjIwNTYsImp0aSI6IjIyM2I4OWIwNzg1OTQxNTA4N2Q4MmMwM2NlMzQwODJiIiwidXNlcl9pZCI6M30.EiIDZCDEbqV2YpX5E8WBC8nHzgGCORjAxKVGWfc2q5U"
}

```
-------------------

``` api/v1/books/ ``` 

Los usuarios normales solo tienen acceso al método GET.
#### Métodos:

*  GET: Devuelve una lista de libros paginados de la siguiente manera: 
```
{
    "total_records": 3,
    "total_pages": 1,
    "current_page": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "El Principito",
            "author": "Antoine de Saint-Exupéry",
            "isbn": "978-8498381498",
            "genre": "Novel",
            "available": true
        },
        {
            "id": 2,
            "title": "Frankenstein",
            "author": "Mary Shelley",
            "isbn": "978-8498381499",
            "genre": "Novel",
            "available": false
        },
        {
            "id": 3,
            "title": "Jurassic Park",
            "author": "Michael Crichton",
            "isbn": "978-849838150",
            "genre": "Science fiction",
            "available": true
        }
    ]
}
```
Permite paginar desde el url usando los parámetros `limit` y `page`.

*  POST: Permite crear un libro. Recibe los datos como JSON de la siguiente manera.

```
{
    "title": "Jurassic Park",
    "author": "Michael Crichton",
    "isbn": "978-849838150",
    "genre": "Science fiction",
}
```
Devuelve una representación JSON del objeto creado.

-------------------

``` api/v1/books/{id}/ ```

Los usuarios normales solo pueden hacer uso del método GET.  

#### Métodos:

* GET: Devuelve el libro que corresponda al ID solicitado.
* PUT: Permite modificar un libro solicitado por ID, solo permite sobreescribir todos los campos. Recibe los datos en formato JSON de la siguiente manera:
```
{
    "title": "Jurassic Park",
    "author": "Michael Crichton",
    "isbn": "978-849838150",
    "genre": "Science fiction",
    "available": false
}

```
Devuelve una representación JSON del objeto modificado.

* PATCH: Permite modificar uno o más atributos de un libro solicitado por ID. Recibe los datos en formato JSON de la siguiente manera:
```
{
    "title": "Jurassic Park"
}
```
Devuelve una representación JSON del objeto modificado.
* DELETE: Permite eliminar un libro solicitado por ID, devuelve una representación JSON del objeto eliminado.

-------------------

``` api/v1/loans/ ```

Todos los usuarios pueden acceder a esta ruta.

### Métodos

* GET: Devuelve todos los prestamos que ha hecho un usuario de la siguiente manera:

```
{
    "total_records": 2,
    "total_pages": 1,
    "current_page": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "loan_date": "2025-02-17T15:58:32.810561Z",
            "return_date": "2025-02-17T16:45:28.113107Z",
            "returned": true,
            "book_id": 1,
            "book_title": "El Principito",
            "book_isbn": "978-8498381498",
            "user_id": 3,
            "user_email": "admin@admin.com"
        },
        {
            "id": 2,
            "loan_date": "2025-02-17T16:37:11.111407Z",
            "return_date": null,
            "returned": false,
            "book_id": 2,
            "book_title": "Frankenstein",
            "book_isbn": "978-8498381499",
            "user_id": 3,
            "user_email": "admin@admin.com"
        }
    ]
}
```

* POST: Permite solicitar un préstamo de libro. Recibe los datos en formato JSON de la siguiente manera: 

```
{
    "book_id": 2,
}
```
No es necesario pasarle el User Id porque lo toma del request, ya que es necesario autenticarse para acceder a cualquier ruta excepto `register/` y las relacionadas a tokens.

-------------------

``` api/v1/returns/ ```

Todos los usuarios pueden acceder a esta ruta.

### Métodos

* POST: Permite regresar un libro previamente prestado. Recibe los datos en formato JSON de la siguiente manera.

```
{
    "book_id": 2,
}
```

Al devolver un libro se actualiza la fecha de devolución del prestamo ligado al usuario, además se vuelve a poner el libro como disponible.


## Cómo ejecutar la aplicación

Para ejecutar la aplicación es necesario tener Docker instalado, una vez hecho esto solo hay que ejecutar el comando `docker compose up` desde la raíz del proyecto. Docker se encargará de levantar las migraciones, así como también de levantar los servicios necesarios. 

Antes de ejecutar el comando `docker compose up` hay que asegurarse de tener el archivo `.env.dev` configurado con los siguientes apartados(pueden cambiarlos a su gusto ya que es un ambiente de desarrollo, pero es necesario que estén todos): 

```
PG_USER=admin
PG_PASSWORD=S3cr3t
PG_DB=library
PG_HOST=db
PG_PORT=5432
```

este archivo debe existir en la raíz del proyecto


### Superusuario
El modelo de usuario utilizado hereda del AbstractUser de Django, por lo tanto, se puede crear un usuario administrador utilizando el comando `docker exec container_name python manage.py createsuperuser`. 

Para saber el nombre del contenedor se puede utilizar el comando
`docker ps -a` el nombre del contenedor está bajo `CONTAINER ID`.

### Autenticación
Para utilizar la mayoría de rutas es necesario contar con un JWT válido. Para obtenerlo es necesario enviar una petición POST con las credenciales del usuario a la ruta `api/v1/token/`. El token tiene una vida útil de 5 minutos, sin embargo, se puede refrescar haciendo uso de la ruta  `api/v1/token/refresh/`.

Para utilizar el token correctamente se debe agregar al header de cualquier petición los siguientes datos.

`Authorization:Bearer {token de acceso}`

### Testing
Para ejecutar las pruebas se debe acceder a la consola del docker container al igual que para crear el superusuario. Habiendo obtenido el container_name se ejecuta docker `exec container_name python manage.py test`.

### Consideraciones
* El servidor de desarrollo de Django no es ideal para ambientes de producción, para este proyecto se utilizó Gunicorn. Es necesario configurar nginx si se quieren manejar archivos estáticos en este API.

* Toda petición que cuente con un body debe ser enviada agregando el '/' al final del URL, esto debido a que Django convierte esta petición en GET si no se envia correctamente. Ejemplo: Para una petición POST user `api/v1/users/` en lugar de `api/v1/users`. 

* Django Rest Framework genera unas páginas mediante las que se puede interactuar con el API, sin embargo, lo mejor es probarla desde un aplicación dedicada a hacer llamados HTTP como POSTMAN.



