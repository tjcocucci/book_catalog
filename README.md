# Videoclub-bookstore

En este proyecto desarrollé dos servicios para una librería y videoclub de mi barrio en Córdoba. Solo consideré la parte del negocio que se dedica a la venta de libros. El primer servicio, `auth` es un sistema básico de autenticación de usuarios. El segundo servicio, `catalog`, es un catálogo de libros. La comunicación entre los servicios está planteada de manera que al consultar el catálogo de libros, el servicio `catalog` verifica que el usuario esté autenticado con el servicio `auth`. Ambos servicios están desplegados en droplets de DigitalOcean. Además, desarrollé un frontend en Next.js para consumir los servicios y lo desplegué en Vercel.

## Direcciones y repositorios

- Servicio `auth`:
  - Dirección: [http://206.81.1.87:4000/docs](http://206.81.1.87:4000/docs)
  - Repositorio: [https://github.com/tjcocucci/catalog_auth](https://github.com/tjcocucci/catalog_auth)
- Servicio `catalog`:
  - Dirección: [http://159.65.225.166:1337/books/](http://159.65.225.166:1337/books/)
  - Repositorio: [https://github.com/tjcocucci/book_catalog](https://github.com/tjcocucci/book_catalog)

- Frontend:
  - Dirección: [https://videoclub-ecru.vercel.app/](https://videoclub-ecru.vercel.app/)
  - Repositorio: [https://github.com/tjcocucci/videoclub-frontend](https://github.com/tjcocucci/videoclub-frontend)

## Servicio `auth`

El servicio `auth` es una API REST implementada en Python con FastAPI. La base de datos es MySQL y se utiliza peewee como ORM. Cuenta con un solo modelo `User` y contamos con endpoints para:

- Crear un usuario (`POST /users`)
- Obtener todos los usuarios (`GET /users`)
- Obtener un usuario por su id (`GET /users/{user_id}`)
- Actualizar un usuario por su id (`PATCH /users/{user_id}`)
- Eliminar un usuario por su id (`DELETE /users/{user_id}`)
- Loguear un usuario y obtener un token de autenticación (`POST /login`)
- Validar un token de autenticación leyendo el header `Authorization` (`GET /session`)

Notar que el endpoint `/users` cuenta con todas las operaciones CRUD para el modelo `User`. El endpoint `/login` utiliza JWT para generar un token de autenticación y el endpoint `/session` decodifica el JWT y verifica que el token sea válido y no haya expirado.

Se puede ver la documentación de la API en el Swagger UI que provee FastAPI en la ruta `/docs`.

Para facliitar la configuración y lanzaiento del servicio, se incluye un archivo `docker-compose.yml` que levanta dos servicios, uno para la aplicación FastAPI y otro para la base de datos MySQL.

## Servicio `catalog`

El servicio `catalog` es una API REST implementada en Python con django y django-rest-framework. La base de datos es MySQL y se utiliza el ORM de django. Cuenta con tres modelos, `Genre`, `Book` y `InventoryItem` con el propósito de que cada libro es registrado como un item en el inventario, de manera que luego podamos extender el sistema para incluir otros tipos de items como películas que también se vendan en el negocio. Cada libro tiene una relación many-to-many con el modelo `Genre`, es decir que un libro puede tener varios géneros y un género puede estar asociado a varios libros. Para generar los endpoints utilicé las vistas genéricas de django-rest-framework `ListCreateAPIView` y `RetrieveUpdateDestroyAPIView` para los tres modelos. con estas vistas completamos todas las operaciones CRUD para los modelos. Los endpoints disponibles son:

- Crear (`POST /genres`), listar (`GET /genres`), obtener por id (`GET /genres/{genre_id}`), actualizar por id (`PATCH /genres/{genre_id}`) y eliminar por id (`DELETE /genres/{genre_id}`) un género
- Crear (`POST /books`), listar (`GET /books`), obtener por id (`GET /books/{book_id}`), actualizar por id (`PATCH /books/{book_id}`) y eliminar por id (`DELETE /books/{book_id}`) un libro
- Crear (`POST /inventory`), listar (`GET /inventory`), obtener por id (`GET /inventory/{inventory_id}`), actualizar por id (`PATCH /inventory/{inventory_id}`) y eliminar por id (`DELETE /inventory/{inventory_id}`) un item de inventario

Para facilitar la configuración y lanzamiento del servicio, se incluye un archivo `docker-compose.yml` que levanta tres servicios, uno para la aplicación django, otro para la base de datos MySQL y un tercero para el servidor web nginx que sirve los archivos estáticos.

## Comunicación entre servicios

Para que el servicio `catalog` pueda verificar que un usuario está autenticado con el servicio `auth`, creamos la clase `AuthServerPermission` extendiendo `BasePermission` en el archivo `permissions.py`. En el método `has_permission` de la clase `AuthServerPermission` hacemos un request `GET` al endpoint `/session` del servicio `auth` con el token de autenticación que viene en el header `Authorization` del request al servicio `catalog`. En todas las vistas utilizamos el campo `permission_classes` para asignar la clase `AuthServerPermission` a las vistas que queremos proteger. De esta manera, si un usuario no está autenticado con el servicio `auth`, obtendrá un error `403` al intentar acceder a las vistas protegidas.

## Frontend

A modo de ejercicio extra, desarrollé un frontend en `Next.js` para consumir los servicios `auth` y `catalog` y lo desplegué en Vercel (shoutout al bootcamp de frontend avanzado que realicé el año pasado en Código Facilito). El frontend es muy básico y por lo pronto solo es para dar un ejemplo de como se pueden consumir los servicios. Cuenta con las siguientes rutas:

- `/`: Página de inicio con un mensaje de bienvenida
- `/login`: Formulario para loguear un usuario
- `/signup`: Formulario para crear un usuario
- `/book-catalog`: Lista de libros del catálogo. A nivel de backend no se puede consumir el servicio de `catalog` sin estar autenticado pero como medida de seguridad adicional, en el frontend se verifica a través del middleware que el usuario esté autenticado para proteger esta ruta

## Mejoras posibles

Hay muchas cosas a mejorar, claro, acá listo algunas ideas, pero antes quiero aclarar que he notado algunos problemas con el contenedor de `mysql` del servicio `auth`. Al principio noté que la conección de `peewee` se caía por algún timeput. Para evitar esto escribí una pequeña función de middleware que inicia una conección en cada hit a la API y la desconecta al terminar de procesarla. Aún así noté que el healthcheck de `docker compose` fallaba al intentar conectarme luego de algunos días. Para intentar resolver este asunto creé un `cronjob` que reinicia los contenedores `unhealthy` mediante la regla:

```bash
* * * * * docker ps -q -f health=unhealthy | xargs docker restart
```

En caso de que alguno de los servicios esté caído me pueden contactar a mi correo `tadeojcocucci@gmail.com`.

### Otras mejoras posibles

- Agregar tests unitarios y de integración
- Incorporar CI/CD
- Automatizar aún más el despliegue
- Automatizar backups de la base de datos

## Testear con curl

Para testear que los servicios funcionan correctamente, podemos utilizar `curl` para hacer requests a los endpoints. A continuación se muestran algunos ejemplos de requests que podemos hacer:

Crear un usuario en el servicio `auth`, reemplazar `$USERNAME` por el nombre de usuario que queremos crear y también la contraseña si queremos cambiarla:

```bash
curl -X 'POST' \
  'http://206.81.1.87:4000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": $USERNAME,
  "password": "Pass123!"
}'
```

Listar todos los usuarios en el servicio `auth`:

```bash
curl -X 'GET' \
  'http://206.81.1.87:4000/users' \
  -H 'accept: application/json'
```

Intentar obtener los libros del servicio `catalog` sin estar autenticado:

```bash
curl -X 'GET' \
  'http://159.65.225.166:1337/books/' \
    -H 'accept: application/json'
```

Loguear un usuario en el servicio `auth` y obtener un token de autenticación, reemplazar `$USERNAME` por el nombre de usuario que queremos loguear y también la contraseña si queremos cambiarla:

```bash
curl -X 'POST' \
  'http://206.81.1.87:4000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "$USERNAME",
  "password": "Pass123!"
}'
```

Ahora utilizar el token de autenticación para obtener los libros del servicio `catalog`, reemplazar `$TOKEN` por el token que obtuvimos en el paso anterior, deberíamos obtener una lista de libros en formato JSON:

```bash
curl -X 'GET' \
  'http://159.65.225.166:1337/books/' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer $TOKEN'
```
