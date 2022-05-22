# API Tareas (tasks)
## Descripción
Una API simple (backend) de un organizador de tareas online (a pequeña escala); puede considerarse una simplificación de Trello. Se conecta a una base de datos de elección y soporta 4 tareas básicas: ver tareas, agregar tarea, modificar y eliminar una tarea. Incluye un sistema de autenticación basado en token. Está construida en FastAPI con diversas herramientas integradas, y puede funcionar como base para una API más grande y con más funcionalidad.

## Instalación
Python (3.6+) es el requisito básico, pero además usamos:
* **pip** instalar dependencias.
* Una base de datos relacional funcionando (localmente o no) con datos de acceso disponibles (aquí se usó **PostgreSQL**, pero no es excluyente).
* Un software como **Postman** para comunicarnos con la API.

Tras bajar el repo, crear un entorno virtual (**venv**) y activarlo (el nombre del entorno no es relevante). En Linux:
```
Python3 -m venv crombie1
source crombie1/bin/activate

```
En Windows con PATH configurado:
```
Python -m venv crombie1
.\crombie1\Scripts\activate
```

Instalar las dependencias:
```
pip install -r requirements.txt
```

Finalmente, ingresar los datos de la BBDD en un archivo **.env** (usamos variables de entorno para datos delicados), usando como ejemplo el archivo **env-sample**.

El servidor se inicia con **uvicorn**, con el comando:
```
uvicorn main:taskApp
```

Los tests unitarios se ejecutan con el comando típico:
```
pytest
```
Los tests no usan la base de datos externa, sino SQLite (para evitar acumulación).

## Endpoints
**Registrar un usuario nuevo**
* La información del usuario va en el *Body*.
* El email es único en la BBDD, pero el nombre de usuario no.
* La API responde con la porción no delicada de los mismos datos, pero no guarda un token (hay que iniciar sesión).

```
POST /usuarios/registrar

Body = {
  "name": {nombre (requerido)},
  "email": {Email (requerido)},
  "password": {Contraseña (requerido)}
}
```

**Iniciar sesión**
* Los datos de la sesión van en el *Body*.
* La API responde con el nombre y el id (para utilidades futuras) y además los codifica en el token.

```
POST /usuarios/entrar

Body = {
  "email": {Email (requerido)},
  "password": {Contraseña (requerido)}
}
```

**Cerrar sesión**
* Una operación simple de eliminación de token.

```
POST /usuarios/salir
```

**Ver todas las tareas.**
* Se puede usar sin un usuario, en cuyo caso sólo se ven las tareas públicas.
* Si hay un usuario, las tareas privadas que se ven son sólo las que le corresponden a dicho usuario.

```
GET /tareas
```

**Ver las tareas en una categoría.**
* Los permisos de los usuarios son los mismos que con el endpoint anterior.
* Las categorías válidas (o *status*, del lado del backend) son 3: *Problemas*, *Trabajando* y *Listo*.

```
GET /tareas/{categoría}
```

**Agregar una tarea.**
* La información de la tarea va en el *Body*.
* El id se crea automáticamente en la base de datos.
* La visibilidad tiene 2 opciones: *Público* y *Privado*. El usuario con sesión activa se considera el *dueño* de la tarea, y por ende el único que puede verla si está configurada como privada.
* La API responde con la información pertinente de la tarea nueva (incluyendo el id del dueño).

```
POST /tareas/

Body = {
  "title": {título (requerido)},
  "description": {descripción (opcional)},
  "status": {estado (requerido)},
  "visibility": {visibilidad (requerido)}
}
```

**Modificar una tarea**
* Se ingresa la categoría deseada y la nueva visibilidad como query parameters (pueden ser los mismos que ya están).
* Sólo el dueño puede modificar una tarea.
* La API responde con la información actualizada de la tarea.

```
PUT /tareas/{id}?category={categoría}&visibility={visibilidad}
```

**Eliminar una tarea**
* Sólo el dueño puede eliminar una tarea.

```
DELETE /tareas/{id}
```

## Detalles de implementación
* El token (**JWT**) se codifica y decodifica directamente en Python, al igual que la contraseña (**Bcrypt**); ambos usan los esquemas de seguridad más recientes, aunque saltándose la solución integral (abstracta) de FastAPI. El token aquí se guarda en una cookie.
* En **config.py**, entre otras cosas, se configura el token, incluyendo el tiempo de expiración (por defecto 24 horas).
* Se hace comprobación de datos con **pydantic** (datos de entrada a la API) y abstracción de la base de datos con **sqlalchemy** (datos de entrada a la BBDD), lo cual explica que haya 2 tipos de modelos separados.
* El manejo de rutas está separado del tratamiento de los datos, a excepción del token (en general, las funciones que interactúan con la base de datos van por separado, y el token no guarda estado).
* Aunque los usuarios y las tareas son los únicos modelos que no pueden faltar, hay mucho desarrollo potencial. Algunas de las cosas que podrían (¿Hipotéticamente?) implementarse en el futuro:
  * Más campos, en especial para las tareas: fecha de finalización, metas parciales, dificultad, etc.
  * Más relaciones entre los usuarios y las tareas: por ejemplo, una lista de colaboradores (lo cual complejizaría el sistema de permisos y visibilidad).
  * Más pasos y mayor seguridad en el sistema de autenticación.
  * Otros tipos de datos, como subtareas y "proyectos" (grupos de tareas), lo cual facilitaría aun más la escalabilidad.
  * Naturalmente, un frontend. No sólo por una cuestión de diseño, sino para poner en práctica el manejo de los códigos de estado HTTP y las redirecciones automáticas.
