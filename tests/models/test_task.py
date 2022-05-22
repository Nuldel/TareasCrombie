import json
import pytest
from data import tasks

# obtener lista de tareas
def test_get_tasks(client):
    response = client.get("/tareas")
    assert response.status_code == 200

# agregar tarea (comprobar persistencia y manejo de sesion)
def test_create_task(client):
    # no se puede agregar una tarea sin un usuario
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200
    body = response.json()
    assert body.get("name") and body["name"] == "FranMa"
    assert body.get("id")
    user_id = body["id"]

    newTask = {"title": "tarea 1",
               "description": "hacer algo",
               "status": "Problemas",
               "visibility": "Público"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    body = response.json()
    assert body.get("title") and body["title"] == "tarea 1"
    assert body.get("description") and body["description"] == "hacer algo"
    assert body.get("status") and body["status"] == "Problemas"
    assert body.get("visibility") and body["visibility"] == "Público"
    assert body.get("owner") and body["owner"] == user_id
    assert body.get("id")
    response = client.get("/tareas")
    assert response.status_code == 200
    assert body in response.json()

    # No debería hacer falta cerrar sesion porque se recarga la api entera

# casos borde: descripcion nula (es opcional), otros campos nulos
def test_create_task2(client):
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200

    newTask = {"title": "tarea 2",
               "description": None,
               "status": "Problemas",
               "visibility": "Público"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    assert response.json()["description"] == None

    newTask = {"title": "tarea 3", "status": "Problemas", "visibility": "Privado"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    assert response.json()["description"] == None

    newTask = {"title": None, "status": "Problemas", "visibility": "Privado"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code != 200

    newTask = {"title": "tarea 5", "status": None, "visibility": "Público"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code != 200

    newTask = {"title": "tarea 5", "status": "Problemas", "visibility": None}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code != 200

    response = client.post("/usuarios/salir")
    assert response.status_code == 200

# casos borde que deben leventar un error
# (notar que todos los campos se convierten a str, así que no hay TypeError)
def test_create_error(client):
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200

    with pytest.raises(ValueError) as error:
        newTask = {"title": "tarea 6", "status": "Retrasado", "visibility": "Público"}
        client.post("/tareas/", json.dumps(newTask))

    with pytest.raises(ValueError) as error:
        newTask = {"title": "tarea 6", "status": "Problemas", "visibility": "public"}
        client.post("/tareas/", json.dumps(newTask))

    with pytest.raises(ValueError) as error:
        newTask = {"title": "tarea 6", "status": 5, "visibility": "Privado"}
        client.post("/tareas/", json.dumps(newTask))

    response = client.post("/usuarios/salir")
    assert response.status_code == 200

# modificar y eliminar tarea
def test_update_task(client):
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200

    newTask = {"title": "tarea 6",
               "description": "Una cosa mas",
               "status": "Problemas",
               "visibility": "Público"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    body = response.json()
    id = body["id"]
    response = client.put(f"/tareas/{id}?category=Trabajando&visibility=Privado")
    assert response.status_code == 200
    assert response.json()["status"] == "Trabajando"
    assert response.json()["visibility"] == "Privado"

    body["status"] = "Trabajando"
    body["visibility"] = "Privado"
    response = client.delete(f"/tareas/{id}")
    assert response.status_code == 200
    response = client.get("/tareas")
    assert body not in response.json()

    response = client.post("/usuarios/salir")
    assert response.status_code == 200

# probar filtro de la BBDD
def test_filter(client):
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200

    for t in tasks:
        response = client.post("/tareas/", json.dumps(t))
        assert response.status_code == 200

    response = client.get("/tareas/Problemas")
    for t in response.json():
        assert t["status"] == "Problemas"

    response = client.get("/tareas/Trabajando")
    for t in response.json():
        assert t["status"] == "Trabajando"

    response = client.get("/tareas/Listo")
    for t in response.json():
        assert t["status"] == "Listo"

    response = client.post("/usuarios/salir")
    assert response.status_code == 200
