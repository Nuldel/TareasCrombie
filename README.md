# API Tareas (tasks)
## Descripción
Una API simple (backend) de un organizador de tareas online; puede considerarse una simplificación de Trello. Se conecta a una base de datos de elección y soporta 4 tareas básicas: ver tareas, agregar tarea, modificar el estado de una tarea y eliminar una tarea. Está construida en FastAPI (Python) con diversas herramientas integradas, y puede funcionar como *boilerplate* para una API más grande y con más funcionalidad.

## Instalación
Python (3.6+) es el requisito básico, pero además usamos:
* **pip** instalar dependencias.
* Una base de datos funcionando (localmente o no) con datos de acceso disponibles (aquí se usó **PostgreSQL**, pero no es excluyente).
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
**Ver todas las tareas.**

```
GET 127.0.0.1:8000/tareas
```

**Ver las tareas en una categoría.**
* Las categorías válidas (o *status*, del lado del backend) son tres: *Problemas*, *Trabajando* y *Listo*.

```
GET 127.0.0.1:8000/tareas/{categoría}
```

**Agregar una tarea.**
* La información de la tarea va en el *Body*.
* El id se crea automáticamente en la base de datos.

```
POST 127.0.0.1:8000/tareas/

Body = {
  "title": {título (requierido)},
  "description": {descripción (opcional)}
  "status": {estado (requerido)}
}
```

**Modificar el estado de una tarea**
* Se ingresa la categoría deseada como query parameter (puede ser la misma que ya está).

```
PUT 127.0.0.1:8000/tareas/{id}?category={categoría}
```

**Eliminar una tarea**

```
DELETE 127.0.0.1:8000/tareas/{id}
```
